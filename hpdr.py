# Calculates and plots the Highest probability density region  (HPDR) of a function 
import numpy as np
import matplotlib.pyplot as plt
import functools as ft
#from useful import MeasureTime
from operator import itemgetter
def comp(*funcs):
    def comp(f1,f2):
        def h(x):
            return f1(f2(x))
        return h
    return ft.reduce(comp,funcs)

def mend_holes(grid,inds): #vytvori intervaly
    inds=sorted(inds)
    
    left_points=[]
    right_points=[]
    left_points.append(grid[inds[0]])
    
    for ind,lastind in zip(inds[1:],inds[:-1]):
        if ind>lastind+1:
            right_points.append(grid[lastind])
            left_points.append(grid[ind])
    right_points.append(grid[inds[-1]])
    return list(zip(left_points,right_points))

def hpdr_o(grid,vals,ɑ=0.05):
    

    tot=0.0
    dh=grid[1]-grid[0]
    xs=[]
    inds=[]
    fsum=np.trapz(vals,grid)
    
    #print(fsum)
    dhs=np.diff(grid)
    dhs=np.append(dhs,dhs[-1])
    while tot<1-ɑ:
        
        ind,q=np.argmax(vals),np.max(vals)
        x=grid[ind]
        #print(q,dhs[ind],fsum)
        #input()
        tot+=q*dhs[ind]/fsum
        xs.append(x)
        inds.append(ind)
        vals[ind]=-5
        #print(tot)
        #input()
    return mend_holes(grid,inds),q

def hpdr(grid,vals,ɑ=0.05):
    
    
    fsum=np.trapz(vals,grid)
    dhs=np.diff(grid)
    dhs=np.append(dhs,dhs[-1])

    allinds=range(len(grid))
    y=np.array(sorted(zip(vals,dhs,allinds),key=itemgetter(0)))
    tots=np.cumsum(y[:,0]*y[:,1])
    #print(fsum)
    #print(tots)
    boundind=np.nonzero(tots>fsum*(ɑ))[0][0]
    q=y[:,0][boundind]
    #print("q:",q)
    inds=y[:,2][boundind:].astype(int)
    return mend_holes(grid,inds),q

def plot_func_and_hpdr(grid,vals,ɑ=0.1):
    intervals,q=hpdr(grid,vals,ɑ=0.1)
    plt.plot(grid,vals)
    #plt.scatter(xs,[q]*len(xs),c="red")
    for xmin,xmax in intervals:
        print(xmin,xmax)
        plt.gca().hlines(q,xmin=xmin,xmax=xmax,linestyles="solid",color="green")
        plt.gca().axvline(xmin,color="green",linestyle="dashed")
        plt.gca().axvline(xmax,color="green",linestyle="dashed")
        draw_arrows(grid,vals,xmin,"right")
        draw_arrows(grid,vals,xmax,"left")
    plt.show()


def draw_arrows(grid,vals,xloc,dir,narr=4,scale=0.008):
    ymin=np.min(vals)
    ymax=np.max(vals)
    size=(np.max(grid)-np.min(grid))*scale
    ylocs=np.linspace(ymin,ymax,narr)
    for yloc in ylocs:
        plt.arrow(xloc,yloc,size*(1 if dir=="right" else -1),0,head_length=0.8*size)
        

grid=np.linspace(0,2*np.pi,10000)
func=comp(lambda x: x**2,np.sin,lambda x: 2*x) #sin(2x)^2
vals=func(grid) #vyhodnocení 
vals=vals/np.trapz(vals,grid) #
plot_func_and_hpdr(grid,vals,ɑ=0.01)
#with MeasureTime():


