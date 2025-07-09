# app.py
import joblib
import numpy as np
import pandas as pd
import os, sys, json
import tensorflow as tf
from typing import Dict, List, Union
from sklearn.compose import _column_transformer as _ct     
from sklearn.base import BaseEstimator, TransformerMixin
from flask import Flask, jsonify, render_template, request
print("TensorFlow version:", tf.__version__)
print("Is GPU available:", tf.config.list_physical_devices('GPU'))

# ────────────────────────────────────────────────────────────────
# 0.  Old-pickle shims  (still required – do NOT remove)
# ────────────────────────────────────────────────────────────────
if not hasattr(_ct, "_RemainderColsList"):
    class _RemainderColsList(list):
        """stub class created by sklearn <1.4 – keep for un-pickling"""
        pass
    _ct._RemainderColsList = _RemainderColsList


class LogScaling(BaseEstimator, TransformerMixin):            
    """Legacy no-op transformer; kept solely so that REALLY old
       pre-processor pickles can still be imported without crashing."""
    def __init__(self, cols=None, eps: float = 1e-6):
        self.cols, self.eps = cols, eps

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X

# ────────────────────────────────────────────────────────────────
# 1.  Paths
# ────────────────────────────────────────────────────────────────
PROJECT_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR    = os.path.join(PROJECT_DIR, "model")

PREPROC_PATH = os.path.join(MODEL_DIR, "preprocessor.joblib")
MODEL_PATH   = os.path.join(MODEL_DIR, "laptop_cost_model.h5")
META_PATH    = os.path.join(MODEL_DIR, "meta.json")

# ────────────────────────────────────────────────────────────────
# 2.  Load artefacts
# ────────────────────────────────────────────────────────────────
try:
    preprocessor = joblib.load(PREPROC_PATH)
    print(f"✔ pre-processor loaded  →  {PREPROC_PATH}", file=sys.stderr)
except Exception as exc:
    raise RuntimeError(f"Could not load pre-processor: {exc}") from exc

try:
    model: tf.keras.Model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print(f"✔ keras model loaded    →  {MODEL_PATH}", file=sys.stderr)
except Exception as exc:
    raise RuntimeError(f"Could not load keras model: {exc}") from exc


# ────────────────────────────────────────────────────────────────
# 3.  Column / category metadata  (comes from meta.json)
# ────────────────────────────────────────────────────────────────
with open(META_PATH, encoding="utf-8") as fh:
    RAW_COLS: List[str] = json.load(fh)["raw_cols"]

NUMERIC_INPUTS = ["Number of Ratings", "Number of Reviews"]
FIXED_NUMS: Dict[str, float] = {
    "Number of Ratings": 300.0,
    "Number of Reviews":  36.0,
}

CATEGORICAL_INPUTS: List[str] = [
    "brand", "processor_brand", "processor_name", "processor_gnrtn",
    "ram_gb", "ram_type", "ssd", "hdd", "os", "os_bit",
    "graphic_card_gb", "weight", "warranty", "Touchscreen",
    "msoffice", "rating"
]

ALL_RAW_INPUTS = NUMERIC_INPUTS + CATEGORICAL_INPUTS            


# ────────────────────────────────────────────────────────────────
# 4.  Flask helpers
# ────────────────────────────────────────────────────────────────
def _missing(col: str):
    return jsonify({"error": f"Missing field: {col}"}), 400

def _bad_numeric(col: str, val: str):
    return jsonify({"error": f"Invalid numeric for {col}: {val}"}), 400


# ────────────────────────────────────────────────────────────────
# 5.  Flask routes
# ────────────────────────────────────────────────────────────────
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        raw: Dict[str, Union[str, float]] = {}

        for col in NUMERIC_INPUTS:
            val = request.form.get(col, "")
            if val in ("", None):
                raw[col] = FIXED_NUMS[col]                
            else:
                try:
                    raw[col] = float(val)
                except ValueError:
                    return _bad_numeric(col, val)

        for col in CATEGORICAL_INPUTS:
            val = request.form.get(col, None)
            if val in ("", None):
                return _missing(col)
            raw[col] = val.strip()

        df_raw  = pd.DataFrame([raw])
        X_trans = preprocessor.transform(df_raw)

        pred = float(model.predict(X_trans, verbose=0)[0, 0])
        return jsonify({"predicted_price": round(pred, 2)})

    except Exception as exc:
        print("↯  error during /predict:", exc, file=sys.stderr, flush=True)
        return jsonify({"error": str(exc)}), 500


# ────────────────────────────────────────────────────────────────
# 6.  Dev server
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
