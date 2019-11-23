from flask_cors import CORS, cross_origin
from flask import jsonify,json
import os
from services import FactCheckingServices,ClaimServices
from app import app

from routes import *



# @app.route('/download',methods=['GET'])
# def getSnapshot():
#     filename = session.get("filename") if session.get("filename") is not None else "default.json"
#     filename = filename[:-4] + 'csv'
#     path_file = os.path.join(app._static_folder,'data',filename)
#     return send_file(path_file,as_attachment=True)


# @app.route('/process',methods=['GET','POST'])
# def process():
#     content = request.form
#     claimId = content["claimId"]
#     cred = content["Credibility"]
#     FactCheckingServices.inferrence(claimId,cred)
#     return redirect('/')


# @app.route("/conservation",methods=['GET'])
# def neuron():
#     return render_template("conversation.html")

# @app.route("/sources",methods=['GET'])
# def getAllSources():
#     FactCheckingServices.getAllSources(session["filename"])
#     return jsonify({"success":True})

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True, host="localhost", threaded=True, port=5050)

