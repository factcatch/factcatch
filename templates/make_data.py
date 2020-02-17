import pandas as pd 
import numpy as np 
import random

group = []
variable = []
value = []

col = 1000
row = 30

group = [int(i/row) for i in range(col*row)]
variable = [(i%row) for i in range(col*row)]
value = [random.randint(0,100) for i in range(col*row)]

df = pd.DataFrame({'group':group,'variable':variable,'value':value})
print(df.shape)
df.to_csv('./data.csv',index=False)