from flask import Flask, render_template, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from app.config import AppConfig

app = Flask(__name__,template_folder='../templates',static_folder="../static/")

app.config.from_object(AppConfig)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'}

db = SQLAlchemy(app)

from app import models
models.db.create_all()
