from app import app
from flask import jsonify,render_template,json
from services import SourceServices

@app.route("/sources",methods=['GET'])
def getAllSources():
    sources = SourceServices.getAllSources()
    return jsonify(sources)

@app.route("/source/claim", methods=["GET"])
def getSourceClaim():
    sources = SourceServices.getSourceClaim()
    return jsonify(sources)

@app.route('/source/getMatrixData')
def getMatrixData():
    links = SourceServices.getLinksMatrix()
    nodes = SourceServices.getNodesMatrix()
    return jsonify({"links":links,"nodes":nodes})
