from flask import url_for,current_app
import os
import json
import pandas as pd
import random


def getData(filename):
    pathFile = os.path.join(current_app._static_folder,'data',filename) 
    with open(pathFile) as blog_file:
        datasets = json.load(blog_file)
        # for id,d in enumerate(datasets):
                # datasets[id]["Tags"] = datasets[id]["Tags"].split(";")[:-1]
        return datasets

def getDataFrame(filename,start,end):
    df_filename = os.path.join(current_app._static_folder,'data',filename[:-4] + 'csv')
    df_gg_filename = os.path.join(current_app._static_folder,'data',filename[:-5] + '_google_results.csv')   
    try:
        df = pd.read_csv(df_filename,encoding='utf-8')
        df_gg = pd.read_csv(df_gg_filename,encoding='utf-8')
        df = df.fillna('')
        df_gg = df_gg.fillna('')
    except:
        df,df_gg = generateDataframe(filename)
    return df.to_dict('records')[start:end],df_gg


def generateDataframe(filename):
    data = getData(filename)
    claim = []
    googleData = []
    for d in data:
        prob = random.uniform(0,1)
        d["Prob"] = round(prob,2)
        d["Credibility"] = round(prob)
        google_results = d["Google Results"]
        for page in google_results:
            results = page["results"]
            for result in results:
                result["Claim_ID"] = d["Claim_ID"]
                googleData.append(result)
        claim.append(d)
    df = pd.DataFrame(claim)
    df_gg = pd.DataFrame(googleData)
    df_filename = os.path.join(current_app._static_folder,'data',filename[:-4] + 'csv')
    df_gg_filename = os.path.join(current_app._static_folder,'data',filename[:-5] + '_google_results.csv')
    df.to_csv(df_filename,index=False)
    df_gg.to_csv(df_gg_filename,index=False)
    return df,df_gg


def getTopClaim(filename,startId,endId):
    data , googleResults = getDataFrame(filename,startId,endId)
    for id,d in enumerate(data):
        data[id]["Tags"] = str(data[id]["Tags"]).split(";")[:-1]
        data[id]["Google Results"] = json.dumps(generateGraph(googleResults.loc[googleResults["Claim_ID"] == d["Claim_ID"]]))
        domains = googleResults.loc[googleResults["Claim_ID"] == d["Claim_ID"]]
        sources = set()
        for idx,row in domains.iterrows():
            sources.add(row["domain"])
        sources = list(sources)
        data[id]["Sources Relation"] = json.dumps(getSources(sources,googleResults))
    return data

def generateGraph(df_gg):
    sources_domain = set()
    docs_link = set()
    for index,row in df_gg.iterrows():
        sources_domain.add(row["domain"])
        docs_link.add(row["link"])
    sources_domain = list(sources_domain)
    docs_link = list(docs_link)
    nodes = [dictNode(s,1,round(random.uniform(0,1),2)) for s in sources_domain]
    sources_domain.extend(docs_link)
    nodesDoc = [dictNode(d,2,100) for d in docs_link]
    nodes.extend(nodesDoc)
    nodes.append(dictNode("claim",3,100))
    links = []
    for index,row in df_gg.iterrows():
        idSource = sources_domain.index(row["domain"])
        idTarget = sources_domain.index(row["link"])
        idClaim = len(sources_domain)
        link = dictLink(idSource,idTarget)
        linkDocClaim = dictLink(idTarget,idClaim)
        links.append(link)
        links.append(linkDocClaim)

    return {"nodes":nodes,"links":links}


def dictNode(label,layer,reliability):
    return {
        "label" : label,
        "layer" : layer,
        "reliability" : reliability*100
    }

def dictLink(source,target):
    return {
        "source" : source,
        "target" : target,
        "value" : 50
    }

def getSources(sources,df):
    nodes = []
    claims = set()
    for source in sources:
        items = []
        items.append(random.randint(100,200))
        items.append(source)
        df_claim = df.loc[df["domain"] == source]
        links = []
        for id,row in df_claim.iterrows():
            links.append(row["Claim_ID"])
        items.append(links)
        nodes.append(items)
    return nodes

def getSourceRelation(sources,df):
    episodes = []
    claims = set()
    for id,source in enumerate(sources):
        df_claim = df.loc[df["domain"] == source]
        if df_claim.shape[0] <= 1:
            continue
        links = []
        for id,row in df_claim.iterrows():
            links.append(row["Claim_ID"])
            claims.add(row["Claim_ID"])
        episodes.append({
            "type" : "episode",
            "name" : source,
            "description": "",
            "episode" : id+1,
            "date" : "",
            "slug" : "episode-one-reverend-john-fife",
            "links" : links
        })
    claims = list(claims)
    themes = []
    for claim in claims[:int(len(claims)/2)]:
        themes.append({
            "type" : "theme",
            "name" : claim,
            "description" : "",
            "slug" : "collapse-2"
        })
    perspectives = []
    for claim in claims[int(len(claims)/2):]:
        perspectives.append({
            "type" : "perspective",
            "name" : claim,
            "descripttion" : "",
            "slug" : "anthropocentric-value-source",
            "count" : random.randint(0,50),
            "group" : 381#random.randint(0,500)
        })
    return {"episodes" : episodes, "themes" : themes, "perspectives" : perspectives}

def inferrence(claimId,cred):
    print(claimId,cred)