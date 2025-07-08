import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent        # …/Laptop-Cost-Evaluation-Project
if ROOT.as_posix() not in sys.path:
    sys.path.append(ROOT.as_posix())

from app import app as flask_app                     # <- the object created in app.py

from vercel_wsgi import handle                       # pip install vercel-wsgi

def handler(event, context):
    """Vercel invokes this function for every request"""
    return handle(flask_app, event, context)

if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=5000)