import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import sys
import os
import random
og=pd.read_csv("o-gold.csv")
ng=pd.read_csv("new_gold.csv")
ob=pd.read_csv("bite.csv")
nb=pd.read_csv("new_bite.csv")
def doit(gen,gj,bj):
    #这是利率
    tg=1
    tb=0
    #这是日期的两个指针
    now_gd=0
    now_bd=0
    #这是当前持有的货币的价格
    now_g=0
    now_b=0
    #这是当前持有的货币的数量
    now_d=1000
    
    ## 其中1代表买，二代表卖，0代表不动
    for tb in range(1,len(nb)-1):
        flag_change=0
        flag_g=0
        flag_b=0
        if now_d!=0:
            if ng.iloc[tg]['ds']==nb.iloc[tb]['ds']: 
                flag_change=1
                if ng.iloc[tg+1]['y']>og.iloc[tg]['y'] and og.iloc[tg-1]['y']>og.iloc[tg]['y']:
                    flag_g=1
            if nb.iloc[tb+1]['y']>ob.iloc[tb]['y'] and ob.iloc[tb-1]['y']>ob.iloc[tb]['y'] :
                flag_b=1
        if now_g!=0:
            if ng.iloc[tg]['ds']==nb.iloc[tb]['ds']: 
                if ng.iloc[tg+1]['y']<og.iloc[tg]['y'] and og.iloc[tg-1]['y']<og.iloc[tg]['y']:
                    if og.iloc[tg]['y']*now_g*(1-gj)>gen[1]*now_gd:
                        flag_g=2
        if now_b!=0:
            if nb.iloc[tb+1]['y']<ob.iloc[tb]['y'] and ob.iloc[tb-1]['y']<ob.iloc[tb]['y']:
                if ob.iloc[tb]['y']*now_b*(1-bj)>gen[2]*now_bd:
                    flag_b=2
        flag_do=0
        if flag_g==1 and flag_b==1 :
            flag_do=1
            if(now_d!=0):
                now_g+=(now_d*gen[0])/(og.iloc[tg]['y']*(1+gj))
                now_gd+=now_d*gen[0]
                now_b+=(now_d*(1-gen[0]))/(ob.iloc[tb]['y']*(1+bj))
                now_bd+=now_d*(1-gen[0])
                now_d=0
        if flag_g==2 and flag_b==1 :
            flag_do=1
            now_gd=0
            now_d+=now_g*(1-gj)*og.iloc[tg]['y']
            now_g=0
            now_b+=(now_d*(1-gen[0]))/(ob.iloc[tb]['y']*(1+bj))
            now_bd+=now_d*(1-gen[0])
            now_d-=(now_d*(1-gen[0]))
        if flag_g==1 and flag_b==2 :
            flag_do=1
            now_g+=(now_d*gen[0])/(og.iloc[tg]['y']*(1+gj))
            now_gd+=now_d*gen[0]
            now_d-=now_d*gen[0]
            now_bd=0
            now_d+=now_b*(1-bj)*ob.iloc[tb]['y']
            now_b=0
        if flag_g==2 and flag_b==2 :
            flag_do=1
            now_gd=0
            now_d+=now_g*(1-gj)*og.iloc[tg]['y']
            now_g=0
            now_bd=0
            now_d+=now_b*(1-bj)*ob.iloc[tb]['y']
            now_b=0
        if flag_do==0:
            if flag_g==1:
                now_g+=(now_d*gen[0])/(og.iloc[tg]['y']*(1+gj))
                now_gd+=now_d*gen[0]
                now_d-=now_d*gen[0]
            if flag_g==2:
                now_gd=0
                now_d+=now_g*(1-gj)*og.iloc[tg]['y']
                now_g=0
            if flag_b==1:
                now_b+=(now_d*(1-gen[0]))/(ob.iloc[tb]['y']*(1+bj))
                now_bd+=now_d*(1-gen[0])
                now_d-=(now_d*(1-gen[0]))   
            if flag_b==2:
                now_bd=0
                now_d+=now_b*(1-bj)*ob.iloc[tb]['y']
                now_b=0
        if flag_change==1:
            tg+=1
    if now_g!=0:
        now_d+=now_g*1794.6*(1-gj)
    if now_b!=0:
        now_d+=now_b*46368.69*(1-bj)
    return now_d

def bianyi(agw):
    now=100.0
    while agw[0]+now>1.0 or agw[0]+now<0.0 :
        now=random.uniform(-0.1,0.1)
        continue;
    agw[0]+=now
    now=100
    while agw[1]+now>5.0 or agw[1]+now<1.0 :
        now=random.uniform(-0.1,0.1)
        continue
    agw[1]+=now
    now=100
    while agw[2]+now>5.0 or agw[2]+now<1.0 :
        now=random.uniform(-0.1,0.1)
        continue
    agw[2]+=now
    return 1
def yichuan(x):
    gj=x
    bj=2*x
    list_ans=[]
    list_best=[]
    gen=[]
    a=[0.5,1.5,1.5]
    gen.append(a)
    best=[a,doit(a,gj,bj)]
    for i in range(0,100):
        print(i)
        gennew=[]
        for j in gen:
            for k in range(0,3):
                tmpl=j[:]
                bianyi(tmpl)
                gennew.append(tmpl[:])
        gen=gennew
        tm=pd.DataFrame(columns=['a','b'])  
        for j in gen :
            tmp=doit(j,gj,bj)
            print(tmp)
            no=[j[:],tmp]
            tm.loc[len(tm)]=no[:]
            if tmp>best[1]:
                best=no[:]
        tm=tm.sort_values(by=['b'],ascending = False)
        gen=[]
        for i in range(0,2):
            gen.append(tm.iloc[i]['a'])
        list_ans.append(tm.iloc[0]['b'])
        list_best.append(best[1])
    list=best[0]
#    plt.plot(list_ans)
#    plt.plot(list_best)
#    plt.show()
    print()
    for i in range(0,3):
        print(best[0][i])
    print(best[1])
    print()
    return best
num_a=[]
for ne_X in range(0,10):
    print()
    print(ne_X)
    print()
    z=ne_X/100.0
    z=z*2
    tmpq=yichuan(z)
    num_a.append(tmpq)
Dp=pd.DataFrame(columns=[0,1,2])
Dd=[]
Df=pd.DataFrame(num_a)
for i in range(0,len(Df)):
    Dp.loc[len(Dp)]=Df.iloc[i][0]
    Dd.append(Df.iloc[i][1])
p=[]
gp=[]
bp=[]
for i in range(0,len(Dp)):
    p.append(Dp.iloc[i][0])
    gp.append(Dp.iloc[i][1])
    bp.append(Dp.iloc[i][2])
plot_s=[(i/100.0)*2 for i in range(0,10)]
plt.plot(plot_s,Dd)
plt.show()
plt.plot(plot_s,p)
plt.show()
plt.plot(plot_s,gp)
plt.show()
plt.plot(plot_s,bp)
plt.show()