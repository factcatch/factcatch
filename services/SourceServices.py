from app.models import Claim,GoogleResult
from app import db
import random
import json

# def getAllSources():
#     sources = GoogleResult.query.with_entities(GoogleResult.claim_id,GoogleResult.domain).distinct().all()
#     results = []
#     for id,source in enumerate(sources):
#         sourceClaim = []
#         sourceClaim.append(source[1])
#         claims = Claim.query.filter_by(id=source[0]).all()
#         for idc, claim in enumerate(claims):
#             claims[idc].documents = [] 
#         sourceClaim.append(claims)
#         results.append(sourceClaim)
#     return results

def sortSource(source):
    return len(source[1])

def getAllSources():
    domains = GoogleResult.query.with_entities(GoogleResult.domain).distinct().all()
    results = []
    for domain in domains:
        claimsId = GoogleResult.query.with_entities(GoogleResult.claim_id).filter_by(domain=domain).all()
        sourceClaim = []
        sourceClaim.append(domain[0])
        claims = []
        for claim in claimsId:
            claim = Claim.query.filter_by(id=claim[0]).first()
            # claim.tags = claim.tags.split(";")
            claim.documents = []
            claims.append(claim)
        sourceClaim.append(claims)
        results.append(sourceClaim)
    results.sort(key=sortSource,reverse=True)
    return results

def getSourcesWithClaim():
    domains = GoogleResult.query.with_entities(GoogleResult.domain).distinct().all()
    results = []
    max_index = 0
    sources = []
    for domain in domains:
        claimsId = GoogleResult.query.with_entities(GoogleResult.claim_id).filter_by(domain=domain).all()
        # sourceClaim = []
        # sourceClaim.append(domain[0])
        # claims = []
        if len(claimsId) < 2:
            continue
        sources.append(domain[0])
        # print(len(claimsId))
        credibilitySource = random.randint(10,50) 
        for index,claim in enumerate(claimsId):
            claim = Claim.query.with_entities(Claim.claim).filter_by(id=claim[0]).first()
            # claim.tags = claim.tags.split(";")
            # claims.append(claim[0])
            results.append({
                "source" : domain[0],
                "claim" : claim[0],
                "index" : index,
                "credibility_claim" : credibilitySource
            })
            max_index = max(max_index,index)
        # sourceClaim.append(claims)
        # results.append(sourceClaim)
    # results.sort(key=sortSource,reverse=True)
    return {
        "max_index" : max_index,
        "sources" : sources,
        "relations" : results   
    }

