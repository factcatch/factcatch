from app.models import Claim, GoogleResult
from app import db
import random
import json
import math
from collections import OrderedDict
from sqlalchemy import func


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
                Claim.query.with_entities(Claim.id, Claim.claim,Claim.credibility)
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
                    "credibility_claim": claim[2]
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

# def getSourceHasGreaterNumClaims():
    # domains = GoogleResult.query.with_entities(GoogleResult.domain).distinct().all()
    # query = 
    # results = []
    # for domain in domains:
    #     if domain[0] == "":
    #         continue
    #     total =  GoogleResult.query.filter_by(domain=domain).count() #random.randint(100, 200)
    #     credibility = GoogleResult.query.join(Claim).filter(GoogleResult.domain==domain,Claim.credibility==1).count() #Claim.query.filter_by(credibility=1).count() #random.randint(0, 100)
    #     uncredibility = GoogleResult.query.join(Claim).filter(GoogleResult.domain==domain,Claim.credibility==0).count() #random.randint(0, 100)
    #     claimsId = (
    #         GoogleResult.query.with_entities(GoogleResult.claim_id)
    #         .filter_by(domain=domain[0])
    #         .all()
    #     )
    #     if len(claimsId) < 5:
    #         continue


def getSourceClaim():
    domains = GoogleResult.query.with_entities(GoogleResult.domain).distinct().all()
    results = []
    for domain in domains:
        if domain[0] == "":
            continue
        total =  GoogleResult.query.filter_by(domain=domain).count() #random.randint(100, 200)
        credibility = GoogleResult.query.join(Claim).filter(GoogleResult.domain==domain,Claim.credibility==1).count() #Claim.query.filter_by(credibility=1).count() #random.randint(0, 100)
        uncredibility = GoogleResult.query.join(Claim).filter(GoogleResult.domain==domain,Claim.credibility==0).count() #random.randint(0, 100)
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
                Claim.query#.with_entities(Claim.id, Claim.claim)
                .filter_by(id=claim[0])
                .first()
            )
            claims.append({
                "claim_id" : claim.id,
                "claim" : claim.claim,
                "credibility_claim" : claim.credibility #10 - index if 10 - index >= 0 else 0
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

def getLinksMatrix():
    # links = db.session.query(GoogleResult.domain,GoogleResult.claim_id).group_by(GoogleResult.domain).having(func.count(GoogleResult.claim_id) > 5).all()
    # links = GoogleResult.query.with_entities(GoogleResult.domain,GoogleResult.claim_id).all()
    domains = GoogleResult.query.with_entities(GoogleResult.domain).group_by(GoogleResult.domain).having(func.count(GoogleResult.claim_id) > 5).all()
    domains = [x for x, in domains]
    links = GoogleResult.query.filter(GoogleResult.domain.in_(domains)).all()
    results = []
    for link in links:
        results.append({
            'source' : link.domain,
            'target' : link.claim_id,
            'value' : 1
        })

    return results

def getNodes():
    domains = GoogleResult.query.with_entities(GoogleResult.domain).distinct().all()
    domains = GoogleResult.query.with_entities(GoogleResult.domain).group_by(GoogleResult.domain).having(func.count(GoogleResult.claim_id) > 5).all()
    print(domains)
    claims = GoogleResult.query.with_entities(GoogleResult.claim_id).distinct().all()
    print(len(claims))
    results = []
    for domain in domains:
        results.append({
            'name' : domain[0],
            'group' : random.randint(0,5),
            'category' : 'source'
        })
    for claim in claims:
        results.append({
            'name' : claim[0],
            'group': random.randint(0,5),
            'category' : 'claim'
        })

    return results

def calculateEntropy(p):
    return 0 if (p==0 or p==1) else float("{0:.2}".format(p*math.log(p) - (1-p)*math.log(1-p)))


def getNodesMatrix():
    query = """
    SELECT * FROM (
        SELECT 
            domain,claim_id,prob_model,count(claim_id) 
                over (partition by domain) as num_claims
        FROM google_result,claim
        WHERE google_result.claim_id = claim.id
        ) as T
    WHERE T.num_claims > 5
    """
    result = db.session.execute(query)
    nodes = []
    # print(result)
    for r in result:
        nodes.append({
            'name': r[0],
            'group' : r[3],
            'category' : 'source'
        })
        nodes.append({
            'name': r[1],
            'group' : calculateEntropy(float(r[2])),
            'category' : 'claim'
        })
    nodes = [dict(t) for t in {tuple(d.items()) for d in nodes}]
    print('set node',len(list(nodes)))
    return list(nodes)