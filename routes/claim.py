from app import app
from flask import jsonify,render_template,json
from services import ClaimServices,SourceServices

@app.route("/claim",methods=['GET'])
def hello():
    return render_template("demo.html")

@app.route("/",methods=['GET'])
def getAllClaim():
    claims = ClaimServices.getAllClaims()
    claims = json.dumps(claims)
    claims = json.loads(claims)
    sources = [] #SourceServices.getAllSources()
    sources = json.dumps(sources)
    sources = json.loads(sources)
    analysis = ClaimServices.analysis()
    if len(claims) == 0:
        return render_template("getstarted.html")
    return render_template("home.html",data=claims,sources=sources,analysis=analysis)

@app.route('/claim/getUserCredAndModel')
def getUserCredAndModel():
   result = ClaimServices.getUserCredAndModel()
   return jsonify(result)