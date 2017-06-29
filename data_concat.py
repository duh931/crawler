import pandas as pd
import numpy as np
import glob



allFiles = glob.glob( "*H*.csv")
list=[]
for file in allFiles:
	df=pd.read_csv(file)
	df.columns=['date',file[:-4],'net_worth','net_worth(reinvest)','rate']
	df['date']=df['date']
	list.append(df.iloc[:,[0,1]])


for i in range(1,len(list)):
	list[0]=pd.merge(list[0],list[i],on='date',how='outer')
result=list[0].drop_duplicates()
result.to_csv('out.csv')

# test=pd.merge(list[0],list[1],on='date')
# print test.drop_duplicates(['date'])