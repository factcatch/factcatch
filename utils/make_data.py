import json 
import os
import argparse


def make_data(num_of_claims):
    pathFolder = './../datasets/Snopes'
    datasets = []
    c = 0
    for i in os.listdir(pathFolder):
        c += 1
        pathFile = pathFolder + '/' + i
        with open(pathFile) as blog_file:
            data = json.load(blog_file)
            datasets.append(data)
            print(c)
        if c == num_of_claims:
            with open('./datasets/dataset_' + str(num_of_claims) +  '_claims.json','w') as f:
                json.dump(datasets,f,ensure_ascii=False)
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_of_claims",default=30,type=int)
    args = parser.parse_args()
    make_data(args.num_of_claims)


