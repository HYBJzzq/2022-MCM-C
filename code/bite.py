import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from fbprophet import Prophet
import sys
import os

Sentiment = 'bite.csv'
a='a.csv'
a=pd.read_csv('a.csv')
data = pd.read_csv('bite.csv')
list=[]
for i in range(0,len(data)):
    print(i)
    a.loc[i]=data.loc[i]
    if i==0:
        list.append(data.iloc[i]['y'])
        continue
    if i==1 :
        list.append(data.iloc[i]['y'])
    if i==len(data)-1:
        continue
    df=a
    m=Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=1)
    foreast=m.predict(future)
    list.append(foreast.iloc[i+1]['yhat'])
fina=a[['ds']]
fina.insert(1,'y',list)
fina.to_csv('new_bite.csv',index=False,header=True)
