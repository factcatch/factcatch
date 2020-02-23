from app import app
from services import ClaimServices
from werkzeug.utils import secure_filename
from flask import request, redirect,flash,send_file
import os,pathlib

# UPLOAD_FOLDER = "./static/data/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'}

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
            ClaimServices.saveToDatabase(file)
            filename = secure_filename(file.filename)
            return redirect('/')
@app.route('/download',methods=['GET'])
def getSnapshot():
    try:
        os.remove(app.static_folder + '\snapshot.json')
    except Exception as e:
        pass
    path_to_file = ClaimServices.export_to_json()
    return send_file(path_to_file,as_attachment=True,cache_timeout=-1)