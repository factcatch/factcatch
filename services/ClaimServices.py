from flask import json,jsonify
from app.models import Claim,GoogleResult
from app import db,app
from sqlalchemy.orm import load_only
import random
import pathlib

def getCredibility(credibility):
    credible = -1
    if isinstance(credibility,str):
        if credibility == "false":
            credible = 0
        elif credibility == "true":
            credible = 1
        else:
            credible = -1
    else:
        credible = credibility
    
    return -1 if random.randint(1,10) <= 6 else credible

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
    if "Prob Model" in data:
        claim.prob_model = data["Prob Model"] 
    else:
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
            try:
                for item_result in itemResult:
                    googleResult = getGoogleResultsFromData(item["Claim_ID"],item_result)
                    db.session.add(googleResult)
            except:
                googleResult = getGoogleResultsFromData(item["Claim_ID"],itemResult)
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
    nonValidatedClaims = Claim.query.filter_by(credibility=-1).all()
    uncertainty = 0
    for claim in nonValidatedClaims:
        uncertainty +=  claim.prob_model
    uncertainty = float("{0:.2f}".format(uncertainty*100/remains))
    perCred = float("{0:.2f}".format((float(cred) / (cred + nonCred))*100))
    perNon = float("{0:.2f}".format(100 - perCred))
    return {
        'claims' : claims,
        'remains' : remains,
        'credibility' : cred,
        'perCred' : perCred,
        'nonCredibility' : nonCred,
        'perNonCred' : perNon,
        'uncertainty' : uncertainty
    }

def getUserCredAndModel():
    userCred = db.session.query(Claim.credibility).filter(Claim.credibility>-1).all()
    userCred = [cred for (cred,) in userCred]
    modelProb = db.session.query(Claim.credibility,Claim.prob_model).filter(Claim.credibility > -1).all()
    modelProb = [float("{0:.2f}".format(abs(cred - prob))) for (cred,prob) in modelProb]
    return {
        "userCred" : userCred,
        "modelProb" : modelProb,
    }

def export_to_json():
    path_to_file = app.static_folder + "\snapshot.json"
    query = """
        COPY(
            SELECT 
                json_agg(fact_checking)
            FROM (
                SELECT
                    origins as "Origins",
                    fack_check as "Fact Check",
                    description as "Description",
                    originally_published as "Originally Published",
                    referred_links as "Referred Links",
                    example as "Example",
                    last_updated as "Last Updated",
                    credibility as "Credibility",
                    url as "URL",
                    claim as "Claim",
                    tags as "Tags",
                    prob_model as "Prob Model",
                    claim.id as "Claim_ID",
                    json_agg(json_build_object('results',gg)) as "Google Results"
                FROM claim,(
                    SELECT
                        claim_id,
                        domain,
                        link,
                        link_type
                    FROM 
                        google_result
                    ) gg
                WHERE claim.id = gg.claim_id
                GROUP BY claim.id
            ) fact_checking
        ) TO :path CSV QUOTE '$'
    """
    db.session.execute(query,{'path':path_to_file})
    data = None
    with open(path_to_file) as f:
        data = f.read()
    with open(path_to_file,"w") as f:
        f.write(data[1:-2])        
    return path_to_file

def validateClaim(claim_id,credibility):
    claim = Claim.query.get(claim_id)
    claim.credibility = credibility
    db.session.commit()
    return True

