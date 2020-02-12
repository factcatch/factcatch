import json 
import os,pathlib
import argparse


def make_data(path_datasets,num_of_claims):
    pathFolder = path_datasets
    datasets = []
    file_in_snopes = os.listdir(os.path.join(path_datasets))
    num_of_claims = num_of_claims if num_of_claims != -1 else len(file_in_snopes)
    c = 0
    for i in file_in_snopes:
        c += 1
        pathFile = pathFolder + '/' + i
        with open(pathFile) as blog_file:
            data = json.load(blog_file)
            datasets.append(data)
            print(c)
        if c == num_of_claims:
            name_ = str(num_of_claims) if num_of_claims != len(file_in_snopes) else 'full'
            with open('./datasets/' + name_ +  '_claims_from_snopes_dataset.json','w') as f:
                json.dump(datasets,f,ensure_ascii=False)
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_of_claims",default=30,type=int)
    parser.add_argument("--path_datasets",default='./../datasets/Snopes',type=str)
    args = parser.parse_args()
    make_data(args.path_datasets,args.num_of_claims)


