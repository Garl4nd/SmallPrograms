import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random as rnd
def fact(k):
    if (k==0): return 1
    f=1
    for i in range(k,1,-1):
        f=f*i
    return f

def comb(n,k):
    r=1
    for i in range(n,n-k,-1):
       r=r*i
    return int(r/fact(k))
def binom(n,k,p):
    return comb(n,k)*p**k*(1-p)**(n-k)  
def cbinom(n,p):
    pkgolu=[]
    pkgolu.append(binom(n,0,p))
    for k in range(1,n+1):
        pkgolu.append(pkgolu[-1]+binom(n,k,p))
    return pkgolu
def premizy(p,q,n):
    if (p==0 and q==0) or (p==1 and q==1): return 1.0
    r=0.0
    for i in range(n+1):
       r+=binom(n,i,p)*binom(n,i,q)
    return r
def modpremizy(p,q,n):
    if (p==0 and q==0) or (p==1 and q==1): return 1.0
    r=0.0
    for i in range(int(n/2)):
       r+=binom(n,i,p)*binom(n,i,q)
    return r    
def pvprodlouzeni(p,q):
    if (p==0 and q==0) or (p==1 and q==1): return 0.0
    srady=1.0/(p+q-2*p*q)
    return p*(1-q)*srady    
def modpvprodlouzeni(pvyhry,prem):
    if (pvyhry==0.0): return 0.0
    srady=1.0/(1.0-prem)
    return pvyhry*srady        
def Penalty(p,q,n):
    for el in (p,q,n):
        if (el<0): el=0
    
    if (p==0 and q==0) or (p==1 and q==1): return 0.0
    
    pw=0.0
    maxkgolu=cbinom(n,q)

    for i in range(1,n+1):
        #pl=0.0
      #  for j in range(i):
       #     pl+=binom(n,j,q)
        #    print ('in',i,j,pl)
        
       
        #pw+=binom(n,i,p)*pl   
        pw+=binom(n,i,p)*maxkgolu[i-1]
    #    print ('out',i,pw)        
    pw+=premizy(p,q,n)*pvprodlouzeni(p,q)
    return pw   
def modp(p,pmod,q):
    pravdep={"vyhra":(1-q)*p,"remiza":(1-q)*(1-p)+q*pmod,"prohra":q*(1-pmod)}
    #print(pravdep,sum(pravdep.values()))
    #input()
    return pravdep
def ModPenalty(p,pmod,q,n):
    for el in (p,q,n):
        if (el<0): el=0
    if (p==0 and q==0) or (p==1 and q==1): return 0.0
    
    pravdep=modp(p,pmod,q)
    maxkproher=cbinom(n,pravdep["prohra"])
   # print(maxkproher)
    pw=0.0;
    pr=0.0
    pr+=binom(n,0,pravdep["vyhra"])*binom(n,0,pravdep["prohra"]/(1.0-pravdep["vyhra"]))
    for i in range(1,int(n/2)+1):
        pvvp=cbinom(n-i,pravdep["prohra"]/(1.0-pravdep["vyhra"]))[i-1]
    #    print(i,binom(n,i,pravdep["vyhra"]),pvvp)
        pw+=binom(n,i,pravdep["vyhra"])*pvvp
        pr+=binom(n,i,pravdep["vyhra"])*binom(n-i,i,pravdep["prohra"]/(1.0-pravdep["vyhra"]))
    for i in range(int(n/2)+1,n+1):
        pw+=binom(n,i,pravdep["vyhra"])
    #pw+=modpremizy(pravdep["vyhra"],pravdep["prohra"],n)
    pw+=pr*modpvprodlouzeni(pravdep["vyhra"],pravdep["remiza"])
   # print(pr,modpvprodlouzeni(pravdep["vyhra"],pravdep["remiza"]))
    return pw
#for i in range(6):
    #print(fact(i))
    #print(comb(6,i))
def compare(p,q,n):
    print(p,q,ModPenalty(p,0.9*p,q,n),Penalty(p,q,n))
