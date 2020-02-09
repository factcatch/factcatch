from flask import json,jsonify
from app.models import Claim,GoogleResult
from app import db
from sqlalchemy.orm import load_only
import random

def getCredibility(credibility):
    if credibility == "false":
        return 0
    else:
        return 1

def getClaimFromData(data):
    claim = Claim()
    claim.id = data["Claim_ID"]
    claim.origins = data["Origins"]
    claim.fack_check = data["Fact Check"]
    claim.description = data["Description"]
    claim.originally_published = data["Originally Published"]
    claim.referred_links = data["Referred Links"]
    claim.example = data["Example"]
    claim.last_updated = data["Last Updated"]
    claim.credibility = getCredibility(data["Credibility"])
    claim.claim = data["Claim"]
    claim.tags = data["Tags"]
    claim.url = data["URL"]
    claim.prob_model = float("{0:.2f}".format(random.uniform(0.0, 1.0)))
    return claim

def getGoogleResultsFromData(claim_id,data):
    googleResult = GoogleResult()
    googleResult.claim_id = claim_id
    googleResult.domain = data["domain"]
    googleResult.link = data["link"]
    googleResult.link_type = data["link_type"]
    return googleResult

def cleanDatabase():
    db.session.query(GoogleResult).delete()
    db.session.query(Claim).delete()
    db.session.commit()

def saveToDatabase(file):
    cleanDatabase()
    claims = json.load(file)
    for item in claims:
        claim = getClaimFromData(item)
        googleResults = item["Google Results"]
        for item_gg in googleResults:
            itemResult = item_gg["results"]
            for item_result in itemResult:
                googleResult = getGoogleResultsFromData(item["Claim_ID"],item_result)
                db.session.add(googleResult)
        db.session.add(claim)
    db.session.commit()

def getGoogleResultsClaim(claim_id):
    return GoogleResult.query.filter_by(claim_id=claim_id).all()

def getSourcesRelations(claim_id):
    sources = GoogleResult.query.with_entities(GoogleResult.domain).filter_by(claim_id=claim_id).distinct()#.all()
    nodes = []
    for source in sources:
        items = []
        items.append(random.randint(100,200))
        items.append(source)
        links = GoogleResult.query.with_entities(GoogleResult.claim_id).filter_by(domain=source).all()
        items.append(links)
        nodes.append(items)
    return nodes
            
def getAllClaims():
    claims = Claim.query.all()
    for id,claim in enumerate(claims):
        claims[id].tags = claim.tags.split(";")[:-1]
        claims[id].documents = getSourcesRelations(claim.id)
    return claims

def analysis():
    claims = Claim.query.count()
    remains = Claim.query.filter_by(credibility=-1).count()
    cred = Claim.query.filter_by(credibility=1).count()
    nonCred = Claim.query.filter_by(credibility=0).count()
    # perCred = (float(cred) / claims)*100
    perCred = float("{0:.2f}".format((float(cred) / (cred + nonCred))*100))
    return {
        'claims' : claims,
        'remains' : remains,
        'credibility' : cred,
        'perCred' : perCred,
        'nonCredibility' : nonCred,
        'perNonCred' : 100 - perCred
    }

def getUserCredAndModel():
    userCred = db.session.query(Claim.credibility).all()
    userCred = [cred for (cred,) in userCred]
    modelProb = db.session.query(Claim.credibility,Claim.prob_model).all()
    modelProb = [abs(cred - prob) for (cred,prob) in modelProb]
    return {
        "userCred" : userCred,
        "modelProb" : modelProb,
    }



