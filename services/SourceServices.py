from app.models import Claim,GoogleResult
from app import db

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

