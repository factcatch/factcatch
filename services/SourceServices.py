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
            claim.documents = []
            claims.append(claim)
        sourceClaim.append(claims)
        results.append(sourceClaim)
    results.sort(key=sortSource, reverse=True)
    return results


def getSourceClaim():
    query = """
        SELECT * FROM (
                SELECT 
                    gg.domain,gg.claim_id,c.credibility,c.claim,count(gg.claim_id)
                        over (PARTITION BY gg.domain) as total
                    FROM google_result gg,claim c
                WHERE gg.claim_id = c.id
            ) as T 
        WHERE T.total > 5
    """
    result = db.session.execute(query)
    sources = {}
    for r in result:
        try:
            sources[r[0]]['credibility'] = sources[r[0]]['credibility'] + 1 if r[2] == 1 else sources[r[0]]['credibility']
            sources[r[0]]['uncredibility'] = sources[r[0]]['uncredibility'] + 1 if r[2] == 0 else sources[r[0]]['uncredibility']
            sources[r[0]]['claims'].append({'claim':r[3],'claim_id':r[1],'credibility_claim':r[2]})
        except:
            sources[r[0]] = {}
            sources[r[0]]['source'] = r[0]
            sources[r[0]]['total'] = r[4]
            sources[r[0]]['credibility'] = 1 if r[2] == 1 else 0 
            sources[r[0]]['uncredibility'] = 1 if r[2] == 0 else 0
            sources[r[0]]['claims'] = []
            sources[r[0]]['claims'].append({'claim':r[3],'claim_id':r[1],'credibility_claim':r[2]})

    results = []
    for s in sources.items():
        results.append(s[1])
    return results
        
def getLinksMatrix():
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