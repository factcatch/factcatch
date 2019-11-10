import json 
import os

pathFolder = './../datasets/Snopes'

datasets = []
c = 0
for i in os.listdir(pathFolder):
    c += 1
    pathFile = pathFolder + '/' + i
    with open(pathFile) as blog_file:
        data = json.load(blog_file)
        datasets.append(data)
        # print(data)
    if c == 10:
        with open('datasets.json','w') as f:
            json.dump(datasets,f,ensure_ascii=False)
        break

# datasets = json.dumps(datasets)
# print(datasets[0])
    # print(i)