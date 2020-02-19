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

@app.route("/sc",methods=['GET'])
def getSourcesWithClaim():
    sources = SourceServices.getSourcesWithClaim()
    return jsonify(sources)

@app.route("/source/sort",methods=['GET'])
def getSourceDesc():
    sources = SourceServices.getSourceDesc()
    return jsonify(sources)
    # return jsonify({"success":True})

@app.route("/source/claim", methods=["GET"])
def getSourceClaim():
    sources = SourceServices.getSourceClaim()
    return jsonify(sources)

@app.route('/source/getLinks')
def getLinksMatrix():
    links = SourceServices.getLinksMatrix()
    return jsonify(links)

@app.route('/source/getNodes')
def getNodesMatrix():
    nodes = SourceServices.getNodesMatrix()
    return jsonify(nodes)

@app.route('/source/getMatrixData')
def getMatrixData():
    links = SourceServices.getLinksMatrix()
    nodes = SourceServices.getNodesMatrix()
    return jsonify({"links":links,"nodes":nodes})


@app.route('/source/getN')
def getN():
   SourceServices.getNodes()
   return jsonify({"success":True})