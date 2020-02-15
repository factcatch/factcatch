from app import app
from flask import jsonify,render_template,json,request
from services import ClaimServices,SourceServices

@app.route("/claim",methods=['GET'])
def hello():
    return render_template("demo.html")

@app.route("/",methods=['GET'])
def getDashboard():
    claims = ClaimServices.getAllClaims()
    claims = json.dumps(claims)
    claims = json.loads(claims)
    if len(claims) == 0:
        return render_template("getting_started.html")
    sources = [] #SourceServices.getAllSources()
    sources = json.dumps(sources)
    sources = json.loads(sources)
    analysis = ClaimServices.analysis()
    return render_template("home.html",data=claims,sources=sources,analysis=analysis)

@app.route('/claim/getUserCredAndModel')
def getUserCredAndModel():
   result = ClaimServices.getUserCredAndModel()
   return jsonify(result)

@app.route('/getting-started')
def get_started():
    return render_template("getting_started.html")

@app.route('/claim/getAllClaims',methods=['GET'])
def getAllClaims():
    claims = ClaimServices.getAllClaims()
    claims = json.dumps(claims)
    claims = json.loads(claims)
    return jsonify(claims)

@app.route('/claim/validate',methods=['POST'])
def validateClaim():
    data = request.json
    # print(data)
    ClaimServices.validateClaim(data['id'],data['credible'])
    return jsonify({"success":True})

@app.route('/claim/getAnalysis',methods=['GET'])
def getAnalysis():
    analysis = ClaimServices.analysis()
    analysis = json.dumps(analysis)
    analysis = json.loads(analysis)
    return jsonify(analysis)
   