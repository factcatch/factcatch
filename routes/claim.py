from app import app
from flask import jsonify,render_template,json
from services import ClaimServices

@app.route("/claim",methods=['GET'])
def hello():
    return render_template("demo.html")

@app.route("/",methods=['GET'])
def getAllClaim():
    claims = ClaimServices.getAllClaims()
    claims = json.dumps(claims)
    claims = json.loads(claims)
    if len(claims) == 0:
        return render_template("getstarted.html")
    return render_template("home2.html",data=claims)