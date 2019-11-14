from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, redirect,flash,url_for,session,send_file
from flask import jsonify,json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from werkzeug.utils import secure_filename
import os
from services import FactCheckingServices

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

UPLOAD_FOLDER = "./static/data/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'}


app.config["JSON_AS_ASCII"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "super secret key"


@app.route("/", methods=["GET", "POST"])
def home():
    if session.get("filename") is not None:
        data = FactCheckingServices.getTopClaim(session["filename"],0,30)
    else:
        # data = FactCheckingServices.getFactCandidate("default.json")
        data = FactCheckingServices.getTopClaim("default.json",0,10)
    return render_template("home.html",data=data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            FactCheckingServices.generateDataframe(filename)
            session['filename'] = file.filename
            return redirect('/')

@app.route('/download',methods=['GET'])
def getSnapshot():
    filename = session.get("filename") if session.get("filename") is not None else "default.json"
    filename = filename[:-4] + 'csv'
    path_file = os.path.join(app._static_folder,'data',filename)
    return send_file(path_file,as_attachment=True)


@app.route('/process',methods=['GET','POST'])
def process():
    content = request.form
    claimId = content["claimId"]
    cred = content["Credibility"]
    FactCheckingServices.inferrence(claimId,cred)
    return redirect('/')


@app.route("/neuron",methods=['GET'])
def neuron():
    return render_template("neuron.html")


if __name__ == "__main__":
    CORS(app)
    app.run(debug=True, host="localhost", threaded=True, port=5050)

