from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# database_uri = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
#     dbuser='postgres',
#     dbpass=27101997,
#     dbhost='localhost',
#     dbname='tweets'
# )

app = Flask(__name__)
# app.config.update(
#     SQLALCHEMY_DATABASE_URI=database_uri,
#     SQLALCHEMY_TRACK_MODIFICATIONS=False,
#     PRODUCTION = False,
# )

app.config['JSON_AS_ASCII'] = False


# db = SQLAlchemy(app)


@app.route('/')
def hello():
    return render_template('home.html')

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True, host='localhost', threaded=True, port=5050)