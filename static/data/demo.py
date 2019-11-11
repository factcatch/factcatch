import pandas as pd 

df = pd.read_csv('./datasets4.csv',encoding='utf-8')
df = df.fillna('0')
df.to_csv('demo.csv',index=False)
data = df.to_dict('records')
print(data[2]["Fact Check"])