import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def moving_average(ar,n=2):
    window=np.ones(n)/n
    return np.hstack([[ar[0]]*n,np.convolve(ar,window)[n:]])[:len(ar)]
def pad_and_shift(ar,n):
    newar=np.roll(ar,n)
#    if n!=0:
#        if n<0:
#            newar[n:]=0

    return newar


cf=pd.read_csv("time_series_covid19_confirmed_global.csv")
cd=pd.read_csv("time_series_covid19_deaths_global.csv")
cr=pd.read_csv("time_series_covid19_recovered_global.csv")
#selection=["Czechia","Italy","Germany","China","Japan","France","Spain","Iran","India","China","Sweden","Russia","Canada","US","Korea","Iran","Austria","Poland","Sweden","Norway","Denmark","Belgium"]
only=["Czechia"]#,"Italy","France","Germany","Austria","Poland","Spain"]#"India","Italy","Germany","China","Japan","France","Spain","Iran","India","China","Sweden","Russia","Canada","US","Korea, South","Iran"]#],"Austria","Poland","Sweden","Norway","Denmark","Belgium"
#,"Hungary"]
lr=1
exclude=[]
sellist=[]
dlist=[]
rlist= []
names=[country if type(state) is not str else f"{state}/{country}" for state,country in zip(cf["Province/State"],cf["Country/Region"])]
for ind,ts in cf.iterrows():
    if not any(names[ind].find(sel)!=-1 for sel in exclude):
        sellist.append((names[ind],ts[1],np.array(ts[4:].values,dtype=float)))
        dlist.append((names[ind],cd.iloc[ind][1],np.array(cd.iloc[ind][4:].values,dtype=float)))
        rlist.append((names[ind],cd.iloc[ind][1],np.array(cd.iloc[ind][4:].values,dtype=float)))
sdict={}
ddict={}
rdict={}
for _,country,vals in sellist:
    if country not in sdict:
        sdict[country]=vals
    else:
        sdict[country]+=vals

for _,country,vals in dlist:
    if country not in ddict:
        ddict[country]=vals
    else:
        ddict[country]+=vals
for _,country,vals in rlist:
    if country not in rdict:
        rdict[country]=vals
    else:
        rdict[country]+=vals
if lr>1:
    sdict={key:val[::lr] for key,val in sdict.items() }
    ddict={key:val[::lr] for key,val in ddict.items() }
    rdict={key:val[::lr] for key,val in rdict.items() }

difdict={key:np.diff(vals) for key,vals in sdict.items()}
rwind=3
podil={key:(sdict[key][1:]/sdict[key][:-1].astype(float)) for key,vals in difdict.items()}
ddifdict={key:np.diff(vals) for key,vals in ddict.items()}
dpodil={key:ddict[key][1:]/ddict[key][:-1] for key,vals in difdict.items()}
dovera={key:ddict[key]/(ddict[key]+rdict[key]) for key,vals in difdict.items()}

alguess={}
print(sdict["Czechia"],ddict["Czechia"])
for key,vals in []:#ddict.items():
    l=len(vals)
    ar=np.zeros(l)
    for ind in range(l):
        try:
            ar[ind]=vals[ind+14]*20
        except IndexError:
            for i in range(14):
                ar[ind+i]=ar[ind+i-1]*1.2 
            break
    alguess[key]=ar

plotvars=[sdict,difdict,podil]
dplotvars=[ddict,ddifdict,dpodil]

#only=["Korea"]
titles=["Celkovy pocet potvrzených nakažení", "Denní nárůst","Podil (dnes/včera)"]
for ind,plotvar in enumerate(plotvars):
    fig,_=plt.subplots()
    dar=dplotvars[ind]
    for key,ts in plotvar.items():
        if not any(key.find(word)!=-1 for word in only):
            continue
        plt.plot(ts,".-",label=key)
        plt.plot(moving_average(ts,n=7),color="grey")
        #plt.plot(moving_average(ts,n=3),label=key)
        plt.xlabel(f"<- Čas (dny{'' if lr==1 else f' x {lr} '}) ->")
        #plt.ylabel("<- Počet  ->")
        #plt.plot(dar[key],".-")

    plt.legend()
    plt.yscale("log")
    if ind==0:
        pass#plt.yscale("log")
    plt.title(titles[ind])
plt.show()
exit()
fig,_=plt.subplots()
plotvars2=[dovera,alguess]
legends=["death/infected","interpolace"]
for ind,plotvar in enumerate(plotvars2):
    for key,ts in plotvar.items():
        if key not in only:
            continue
    
        plt.plot(ts,label=f"{key}: {legends[ind]}")
        plt.yscale("log")
plt.legend()

plt.subplots()

n1="Czechia"
cutoff=0
d0=39
a1=sdict[n1][cutoff:]
nind1=np.nonzero(a1)[0][0]
times=range(len(a1))
plt.plot(times,a1,label=n1)

for n2 in  []:#["Germany","Italy","Spain","France","Austria","Sweden","Norway","Denmark"]:
    a2=sdict[n2][cutoff:]
    nind2=np.nonzero(a2>100)[0][0]
    shift=nind2-nind1
    plt.plot(times,pad_and_shift(a2,-shift),label=f"{n2}, shift= {shift}")
    plt.yscale("log")
    plt.legend()
    #cexp=np.array([np.zeros(len(a2)) for _ in range(5)])
    #cexp[:,d0-cutoff]=a2[d0-cutoff]
    #for ind in range(d0+1,len(a2)):
    #    cexp[:,ind]=cexp[:,ind-1]*(1+0.1*np.array(list(range(1,6))))
    
    #cor=np.correlate(a1,a2,mode="full")/np.sqrt((np.correlate(a1,a1))*np.correlate(a2,a2))[0]
    #print(np.argmax(cor),len(cor))
    #shift=-len(cor)//2+np.argmax(cor)
    shift=10#-len(cor)//2+np.argmax(cor)

    
    
    #plt.plot(cor,label=f"Korelace ({n2})")
plt.legend()

plt.show()


