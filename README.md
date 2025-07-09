# Laptop Cost Evaluation Project

[![Laptop Icon](https://raw.githubusercontent.com/Kratugautam99/Laptop-Cost-Evaluation-Project/main/static/icon/laptop_icon.png)](https://github.com/Kratugautam99/Laptop-Cost-Evaluation-Project)

Live Demo → https://laptop-cost-evaluation-project.onrender.com/  

A fast, user-friendly web app that instantly predicts a laptop’s market price from key specs like brand, CPU, RAM, storage, and more.

---
## 📑 Table of Contents

- [🚀 Key Features](#-key-features)  
- [🗂 Project Structure](#-project-structure)  
- [⚙️ Installation & Setup](#installationsetup)  
- [🏃 Usage](#-usage)  
- [📊 Data & Analysis](#-data--analysis)  
- [📋 Requirements.txt](#-requirementstxt)  
- [☁️ Deployment](#deployment)  
- [🔮 Future Work & Ideas](#-future-work--ideas)  
- [🤝 Acknowledgments](#-acknowledgments)  


---
## 🚀 Key Features

- Instant market cost estimation via a clean, single-page form  
- Supports 16 categorical inputs + hidden defaults for ratings & reviews  
- CPU-only TensorFlow backend for lightweight inference  
- Live INR ↔ USD conversion on the client side  
- Portable: runs locally (Windows/WSL/macOS) or on Render with zero-config  

---

## 🗂 Project Structure

```
.
├── app.py
├── laptop_data.csv
├── Laptop_Regression.ipynb
├── README.md
├── requirements.txt
├── model
│   ├── laptop_cost_model.h5
│   ├── meta.json
│   └── preprocessor.joblib
└── static
    ├── css
    │   └── style.css
    ├── icon
    │   └── laptop_icon.png
    ├── img
    │   └── bg.jpg
    └── js
        └── predict.js
```

---
<a id="installationsetup"></a>
## ⚙️ Installation & Setup

Download and Install python 3.10.11 from this [link](https://www.python.org/downloads/release/python-31011/) and Add the path: C:\Users\user(name)\AppData\Local\Programs\Python\Python310\python.exe to Environment Variable (PATH).

### 🟦 PowerShell
```powershell
py -3.10 -m venv tempenv; .\tempenv\Scripts\Activate.ps1
```

---

### 🟠 Git Bash (or any Unix-style shell on Windows)
```bash
python3.10 -m venv tempenv && source tempenv/bin/activate
```

---

### ⚫ CMD (Command Prompt)
```cmd
py -3.10 -m venv tempenv && .\tempenv\Scripts\activate.bat
```

---

## 🏃 Usage

1. Activate your virtual environment  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open your browser at http://localhost:5000

---

## 📊 Data & Analysis

- **laptop_data.csv**  
  Raw dataset of about 1k rows of laptops with specs & prices.  
- **Laptop_Regression.ipynb**  
  Exploratory Data Analysis, feature engineering, model training & evaluation.

Feel free to explore or extend the notebook with new algorithms.

---
## 📋 Requirements.txt

```
# Required for webapp to run
setuptools>=65.0.0
wheel>=0.40.0
Flask==3.1.1
joblib==1.5.1
numpy==2.1.3
pandas==2.3.0
scikit-learn==1.7.0
tensorflow-cpu==2.19.0

# Optional if you want to experiment with Laptop_Regression.ipynb
# lightgbm==4.1.0
# xgboost==1.7.6
# catboost==1.2
# matplotlib==3.7.2
# seaborn==0.12.2
```

---
<a id="deployment"></a>
## ☁️ Deployment

This project is hosted on Render, with following adjustments:

- Set `PYTHON_VERSION=3.10.11` in Render’s Environment tab  
- Bind to the `PORT` env var in `app.py` (fallback to 5000 locally)  
- Static assets served via `{{ url_for('static', …) }}` for correct routing
- ```PROJECT_DIR  = os.path.dirname(os.path.abspath(__file__))``` for relative path in app.py

---

## 🔮 Future Work & Ideas

- Convert the Keras model to **TensorFlow Lite** for ultra-light inference  
- Add real-time currency rates via a free API  
- Build a comparison view: show competitor models & price deltas  
- Expose a public REST API endpoint for batch predictions  

---

## 🤝 Acknowledgments

- Dataset & inspiration provided by [Kaggle](https://www.kaggle.com/datasets/anubhavgoyal10/laptop-prices-dataset)  
- Free hosting and auto-deploy courtesy of [Render](https://render.com/)  
- Interactive development environment powered by [Google Colab](https://colab.research.google.com/) 

Feel free to ⭐ the repo, file issues, or submit PRs for new features!
