from app import app
from flask import jsonify,render_template,json,request
from services import ClaimServices,SourceServices

@app.route("/",methods=['GET'])
def getDashboard():
    if ClaimServices.databaseIsEmpty():
        return render_template("getting_started.html")
    analysis = ClaimServices.analysis()
    return render_template("home.html",analysis=analysis)

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
    ClaimServices.validateClaim(data['id'],data['credible'])
    return jsonify({"success":True})

@app.route('/claim/getAnalysis',methods=['GET'])
def getAnalysis():
    analysis = ClaimServices.analysis()
    analysis = json.dumps(analysis)
    analysis = json.loads(analysis)
    return jsonify(analysis)
   
@app.route('/claim/neural')
def dohits():
    # ClaimServices.doHITS(10)
    # return jsonify({"Success":True})
    return render_template("neural.html")

@app.route('/claim/getHistogram')
def getHistogram():
   histogram = ClaimServices.getHistogram()
   return jsonify({"histogram":histogram})

@app.route('/claim/getNeural')
def getNeural():
    claim_id = request.args.get('id')
    print(claim_id)
    result = ClaimServices.getNeural(claim_id)
    return jsonify(result)

