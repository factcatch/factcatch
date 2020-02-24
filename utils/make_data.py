import json 
import os,pathlib
import argparse


def make_data(path_datasets,num_of_claims):
    pathFolder = path_datasets
    iName = path_datasets.rfind('/') if path_datasets.rfind('/') > 0 else path_datasets.rfind("\\")
    dirDatasets = os.path.join(os.getcwd(),'datasets',path_datasets[iName+1:])
    if not os.path.exists(dirDatasets):
        os.makedirs(dirDatasets)
    datasets = []
    file_in_snopes = os.listdir(os.path.join(path_datasets))
    num_of_claims = num_of_claims if num_of_claims != -1 else len(file_in_snopes)
    c = 0
    for i in file_in_snopes:
        pathFile = pathFolder + '/' + i
        with open(pathFile) as blog_file:
            try:
                data = json.load(blog_file)
                datasets.append(data)
                c += 1
                print(c)
            except:
                pass
        if c == num_of_claims:
            break

    name_ = str(num_of_claims) if num_of_claims != len(file_in_snopes) else 'full'
    name_ = str(c) if c != num_of_claims else name_
    fW = os.path.join(dirDatasets,name_ +  '_claims_from_' + path_datasets[iName + 1:] + '_dataset.json')
    # print(datasets)
    with open(fW,'w') as f:
        json.dump(datasets,f,ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_of_claims",default=30,type=int)
    parser.add_argument("--path_datasets",default='./../datasets/Snopes',type=str)
    args = parser.parse_args()
    make_data(args.path_datasets,args.num_of_claims)


