from flask import url_for,current_app
import os
import json
import pandas as pd


def getData(filename):
    pathFile = os.path.join(current_app._static_folder,'data',filename) 
    with open(pathFile) as blog_file:
        datasets = json.load(blog_file)
        # for id,d in enumerate(datasets):
                # datasets[id]["Tags"] = datasets[id]["Tags"].split(";")[:-1]
        return datasets

def getDataFrame(filename,start,end):
    df_filename = os.path.join(current_app._static_folder,'data',filename[:-4] + 'csv')
    try:
        df = pd.read_csv(df_filename,encoding='utf-8')
        df = df.fillna('')
    except:
        df = generateDataframe(filename)
    return df.to_dict('records')[start:end]

def getFactCandidate(filename):
    data = getData(filename)
    claim = []
    for d in data:
        d["Prob"] = 0.5
        d["Credibility"] = 1
        claim.append(d)
    df = pd.DataFrame(claim)
    df_filename = os.path.join(current_app._static_folder,'data',filename[:-4] + 'csv')
    df.to_csv(df_filename,index=False)
    return df

def generateDataframe(filename):
    data = getData(filename)
    claim = []
    for d in data:
        d["Prob"] = 0.5
        d["Credibility"] = 1
        claim.append(d)
    df = pd.DataFrame(claim)
    df_filename = os.path.join(current_app._static_folder,'data',filename[:-4] + 'csv')
    df.to_csv(df_filename,index=False)
    return df


def getTopClaim(filename,startId,endId):
    data = getDataFrame(filename,startId,endId)
    for id,d in enumerate(data):
        data[id]["Tags"] = str(data[id]["Tags"]).split(";")[:-1]
    return data


def inferrence(claimId,cred):
    print(claimId,cred)
