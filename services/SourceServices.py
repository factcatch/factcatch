from app.models import Claim, GoogleResult
from app import db
import random
import json
from sqlalchemy import func

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
        claimsId = (
            GoogleResult.query.with_entities(GoogleResult.claim_id)
            .filter_by(domain=domain)
            .all()
        )
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
    results.sort(key=sortSource, reverse=True)
    return results


def getEmptyString(n):
    emptyString = ""
    for i in range(n):
        emptyString += " "
    return emptyString


def sortDomain(domain):
    return domain[1]


def getSourceDesc():
    domains = (
        db.session.query(GoogleResult.domain, func.count(GoogleResult.domain))
        .group_by(GoogleResult.domain)
        .all()
    )
    domains.sort(key=sortDomain, reverse=True)
    return domains


def getSourcesWithClaim():
    # domains = GoogleResult.query.with_entities(GoogleResult.domain).distinct().all()
    domains = getSourceDesc()
    domains.sort(key=sortDomain)
    # print(domains)
    results = []
    max_index = 0
    max_cell = 30
    sources = []
    spaces = 1

    for domain in domains:
        # if domain[0] == "www.snopes.com":
        # print("snopes",domain[0])
        total = random.randint(100, 200)
        validation = random.randint(0, 100)
        unvalidation = random.randint(0, 100)
        claimsId = (
            GoogleResult.query.with_entities(GoogleResult.claim_id)
            .filter_by(domain=domain[0])
            .all()
        )
        # sourceClaim = []
        # sourceClaim.append(domain[0])
        # claims = []
        if len(claimsId) < 5:
            continue
        # sources.append(domain[0])
        # print(len(claimsId))
        # credibilitySource = random.randint(10,50)
        for index, claim in enumerate(claimsId):
            claim = (
                Claim.query.with_entities(Claim.id, Claim.claim)
                .filter_by(id=claim[0])
                .first()
            )
            # claim.tags = claim.tags.split(";")
            # claims.append(claim[0])
            # credibilitySource = random.randint(0,10)
            if index == 0:
                sources.append(domain[0])
            if index < max_cell:
                sourceName = domain[0]
            elif index % max_cell == 0:
                spaces += 1
                sourceName = getEmptyString(spaces)
                sources.append(sourceName)
            else:
                sourceName = getEmptyString(
                    spaces
                )  # domain[0] + " " #str(int(index/max_cell))
            results.append(
                {
                    "source_id": 0,
                    "source": sourceName,
                    "total": total,
                    "validation": validation,
                    "unvalidation": unvalidation,
                    "claim_id": claim[0],
                    "claim": claim[1],
                    "index": index % max_cell,
                    "credibility_claim": max_cell - index
                    if max_cell - index >= 0
                    else 0,  # credibilitySource
                }
            )
            max_index = max(max_index, index)
        # sourceClaim.append(claims)
        # results.append(sourceClaim)
    # results.sort(key=sortSource,reverse=True)
    sources.reverse()
    # getSourceDesc()
    # print(sources[0])
    return {"max_index": max_index, "sources": sources, "relations": results}


def getSourceClaim():
    domains = GoogleResult.query.with_entities(GoogleResult.domain).distinct().all()
    results = []
    for domain in domains:
        if domain[0] == "":
            continue
        total = random.randint(100, 200)
        credibility = random.randint(0, 100)
        uncredibility = random.randint(0, 100)
        claimsId = (
            GoogleResult.query.with_entities(GoogleResult.claim_id)
            .filter_by(domain=domain[0])
            .all()
        )
        if len(claimsId) < 5:
            continue
        claims = []
        for index, claim in enumerate(claimsId):
            claim = (
                Claim.query.with_entities(Claim.id, Claim.claim)
                .filter_by(id=claim[0])
                .first()
            )
            claims.append({
                "claim_id" : claim[0],
                "claim" : claim[1],
                "credibility_claim" : 10 - index if 10 - index >= 0 else 0
            })
        results.append(
            {
                "source": domain[0],
                "total": total,
                "credibility": credibility,
                "uncredibility": uncredibility,
                "claims": claims,
            }
        )
    return results
