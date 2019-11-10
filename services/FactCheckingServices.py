from flask import url_for,current_app
import os
import json

def getData(filename):
    pathFile = os.path.join(current_app._static_folder,'data',filename) 
    with open(pathFile) as blog_file:
        datasets = json.load(blog_file)
        for id,data in enumerate(datasets):
                datasets[id]["Tags"] = datasets[id]["Tags"].split(";")[:-1]
        return datasets

def getFactCandidate(filename):
    data = getData(filename)
    return data[:10]

def inferrence(claimId,cred):
    print(claimId,cred)
