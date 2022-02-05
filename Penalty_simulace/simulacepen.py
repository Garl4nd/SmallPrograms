import penmod as pm
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
def simulace(p,pmod,q,n):
    ascore=0
    bscore=0
    i=n-1
    while True:
        #rozstrel
        shoot=rnd.random()
        #print(shoot)
        if (shoot<q): 
            ascore+=1;gol=True
        else:
            gol=False
        shoot=rnd.random()
        #print(shoot)
        if (gol):
            if (shoot<pmod): bscore+=1
        else:
            if (shoot<p):   bscore+=1
        #vyhral nekdo?
        #print(i,ascore,bscore)
        if (i>0): #bezna cast
            rem=i
        else:  # prodlouzeni
            rem=0
        if (ascore-bscore>rem): 
            return 0        
        elif (bscore-ascore>rem): 
            return 1
        i-=1
stat=0.0
#print(simulace(0.9,0.9,0.5,5))        
p=0.7

q=0.5
sc=10
koef=1.0
if (len(sys.argv)>1):
    q=float(sys.argv[1])
if (len(sys.argv)>1):
    koef=float(sys.argv[2])
if (len(sys.argv)>3):
    sc=int(sys.argv[3])
n=5
nt=10000
ns=100

parr=np.linspace(0.1,1.0,sc)

#input()    
fig,ax=plt.subplots()
ax.set_xticks(np.arange(0.0,1.0,0.1))
ax.set_yticks(np.arange(0.0,1.0,0.1))
ax.set_xlabel("p")
ax.set_ylabel("pw")
text=ax.text(0.50, 0.8,'',horizontalalignment='right', fontsize=12,transform=ax.transAxes)

pgarr=np.linspace(0.0,1.0,ns)


pwarr=[]
for i in range(ns):
    pwarr.append(pm.ModPenalty(pgarr[i],pgarr[i]*koef,q,n))

line1=ax.plot(pgarr,pwarr)
vl=[]
count=[]
prop=[]
for i in range(sc):
    vl.append(ax.plot([parr[i],parr[i]],[0,0])[0])
    count.append(0)
    prop.append([])
#line2=ax.plot([],[])
#ax.add_line(line1)
#print(pm.ModPenalty(p,p,q,n))




for i in range(nt):
    for j in range(sc):
        count[j]+=simulace(parr[j],parr[j]*koef,q,n)
        #print(prop[j])
        prop[j].append(count[j]/(1.0*(i+1)))
#print(prop[1:10])
def init():
    
    return [line1[0]]+vl+[text]
def update(iter):
    #line2.clear()
    #print(iter)
    
    #ax.vlines(p,0.0,rnd.random())
    text.set_text("q="+str(q)+", iter= "+str(iter))
    
    for i,l in enumerate(vl):
        l.set_data([parr[i],parr[i]],[0.0,prop[i][iter]])
#    print(prop[iter])
    return [line1[0]]+vl+[text]
    

an=animation.FuncAnimation(fig,update,init_func=init,blit=True,frames=nt,interval=1)
plt.show()