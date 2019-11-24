from app import app
from flask import jsonify,render_template,json
from services import SourceServices

@app.route("/sources",methods=['GET'])
def getAllSources():
    sources = SourceServices.getAllSources()
    return jsonify(sources)
    # return jsonify({"success":True})

@app.route("/sources2",methods=['GET'])
def getAllSources2():
    sources = SourceServices.getAllSources2()
    return jsonify(sources)
    # return jsonify({"success":True})