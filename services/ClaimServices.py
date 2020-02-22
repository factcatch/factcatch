from flask import json,jsonify
from app.models import Claim,GoogleResult
from app import db,app
from sqlalchemy.orm import load_only
import random
import math
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
        claim.prob_model = claim.credibility if claim.credibility > -1 else 0.5
        #float("{0:.2f}".format(random.uniform(0.0, 1.0)))
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
    doHITS(100)

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

def getListClaim():
    claims = Claim.query.all()
    for id,claim in enumerate(claims):
        claims[id].tags = claim.tags.split(";")[:-1]
        claims[id].documents = getNeural(claim.id)
    return claims

def calculateEntropy(p):
    return p if(p==0 or p==1) else - p*math.log(p) - (1-p)*math.log(1-p)

def analysis():
    claims = Claim.query.count()
    remains = Claim.query.filter_by(credibility=-1).count()
    cred = Claim.query.filter_by(credibility=1).count()
    nonCred = Claim.query.filter_by(credibility=0).count()
    sources = GoogleResult.query.with_entities(GoogleResult.domain).distinct().count()
    # perCred = (float(cred) / claims)*100
    nonValidatedClaims = Claim.query.filter_by(credibility=-1).all()
    uncertainty = 0
    for claim in nonValidatedClaims:
        uncertainty +=  calculateEntropy(claim.prob_model)
    uncertainty = float("{0:.2f}".format(uncertainty*100/remains))
    perCred = float("{0:.2f}".format((float(cred) / (cred + nonCred))*100))
    perNon = float("{0:.2f}".format(100 - perCred))
    return {
        'claims' : claims,
        'sources' : sources,
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
    modelProb = db.session.query(Claim).with_entities(Claim.prob_model).all()
    # modelProb = [float("{0:.2f}".format(abs(cred - prob))) for (cred,prob) in modelProb]
    freq = {0.0:0,0.2:0,0.4:0,0.6:0,0.8:0,1.0:0}
    threshold = [0.0,0.2,0.4,0.6,0.8,1.0]
    modelProb = [p for p, in modelProb]
    for p in modelProb:
        for i in range(len(threshold)-1):
            if p >= threshold[i] and p < threshold[i+1]:
                freq[threshold[i]] += 1
                break
    print(freq.items())
        
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
    claim.prob_model = credibility if credibility > -1 else 0.5
    db.session.commit()
    doHITS(10)
    return True

def databaseIsEmpty():
    query = "SELECT count(id) FROM claim"
    result = db.session.execute(query)
    r = [row[0] for row in result]
    return True if r[0] == 0 else False


def doHITS(n):
    resultDB = db.session.query(Claim,GoogleResult).with_entities(Claim.id,Claim.prob_model,Claim.credibility,GoogleResult.domain).filter(Claim.id == GoogleResult.claim_id).all()
    sources = {}
    nSources = {}
    claims = {}
    nClaims = {}
    for t in resultDB:
        try:
            nClaims[t[3]] = nClaims[t[3]] + 1
        except:
            sources[t[3]] = 0
            nClaims[t[3]] = 1

        try:
            nSources[t[0]] = nSources[t[0]] + 1
        except Exception as e:
            nSources[t[0]] = 1
        
        claims[t[0]] = t[1]
        
    for i in range(n):
        for t in resultDB:
            sources[t[3]] += claims[t[0]]/ nClaims[t[3]]
        for c in claims:
            claims[c] = 0
        for t in resultDB:
            claims[t[0]] += sources[t[3]] / nSources[t[0]]
        for s in sources:
            sources[s] = 0

    claimsDB = Claim.query.all()
    for claim in claimsDB:
        claim.prob_model = claims[claim.id] if claim.credibility <0 else claim.credibility
    db.session.commit()

def getHistogram():
    claims = Claim.query.all()
    # histogram = {'0.0':0,'0.1':0,'0.2':0,'0.3':0,'0.4':0,'0.5':0,'0.6':0,'0.7':0,'0.8':0,'0.9':0,'1.0':0}
    histogram = {'0.0':0,'0.2':0,'0.4':0,'0.6':0,'0.8':0}
    for c in claims:
        f = (math.floor(math.floor(c.prob_model*10)/2))/10
        if c.prob_model == 1:
            f = 0.8
        histogram[str(f)] += 1

    return list(histogram.values())

def getNeural_deprecated(claim_id):
    domains = GoogleResult.query.with_entities(GoogleResult.domain).filter_by(claim_id=claim_id).distinct().all()
    rDB = db.session.query(GoogleResult).with_entities(GoogleResult.domain,GoogleResult.claim_id).filter(GoogleResult.domain.in_(domains))
    sources = {}
    claims = {}
    nodes = {}
    for r in rDB:
        try:
            sources[r[0]] = sources[r[0]] + 1
        except:
            sources[r[0]] = 1
        try:
            claims[r[1]] = claims[r[1]] + 1
        except:
            claims[r[1]] = 1
    
    i = 0
    for s in sources:
        nodes[s] = {"name":s,"group" : sources[s],"category" : "source","index" : i}
        i += 1
    for c in claims:
        nodes[c] = {"name":c, "group" : claims[c],"category" : "claim", "index" : i }
        i += 1
    
    # for node in nodes.values():
        # print(node)
    links = []
    for r in rDB:
        links.append({"source":nodes[r[0]]["index"],"target": nodes[r[1]]["index"],"weight":1})
    # for link in links:
    # print('links',links)
    # print('nodes',nodes)
    nodes = [node for node in nodes.values()]
    return {
        'nodes' : nodes,
        'links' : links
    }


def getNeural(claim_id):
    domains = GoogleResult.query.with_entities(GoogleResult.domain).filter_by(claim_id=claim_id).distinct().all()
    rDB = db.session.query(GoogleResult,Claim).with_entities(GoogleResult.domain,GoogleResult.claim_id,Claim.credibility).filter(GoogleResult.domain.in_(domains),GoogleResult.claim_id != claim_id,GoogleResult.claim_id==Claim.id)
    sources = {}
    claims = {}
    nodes = {}
    for r in rDB:
        try:
            sources[r[0]] = sources[r[0]] + 1
        except:
            sources[r[0]] = 1
        # try:
            # claims[r[1]] = claims[r[1]] + 1
        # except:
        claims[r[1]] = r[2]
    
    i = 0
    for s in sources:
        nodes[s] = {"id":i,"name":s,"group" : sources[s],"category" : "source","index" : i}
        i += 1
    for c in claims:
        nodes[c] = {"id":i,"name":c,"group" : claims[c],"category" : "claim", "index" : i }
        i += 1
    
    links = []
    for r in rDB:
        links.append({"source":nodes[r[0]]["id"],"target": nodes[r[1]]["id"],"value":nodes[r[0]]["group"]})
    # print('links',len(links))
    # print('nodes',len(nodes))
    nodes = [node for node in nodes.values()]
    return {
        'nodes' : nodes,
        'links' : links
    }