from flask import Flask, render_template, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

database_uri = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser='postgres',
    dbpass=27101997,
    dbhost='localhost',
    dbname='fact_checking'
)

app = Flask(__name__,template_folder='../templates',static_folder="../static/")
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    PRODUCTION = False,
)


UPLOAD_FOLDER = "./static/data/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'}


app.config["JSON_AS_ASCII"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "super secret key"

db = SQLAlchemy(app)

from app import models
models.db.create_all()
