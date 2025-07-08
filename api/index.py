import os, json, sys
from vercel_wsgi import handle   

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from app import app
def handler(event, context):
    return handle(app, event, context)