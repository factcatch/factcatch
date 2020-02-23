from flask_cors import CORS, cross_origin
from flask import jsonify,json
import os
from services import FactCheckingServices,ClaimServices
from app import app

from routes import *

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True, host="localhost", threaded=True, port=5050)

