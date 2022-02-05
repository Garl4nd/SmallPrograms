import numpy as np
import math
import matplotlib.pyplot as plt
import itertools as it
def naive_dft(a):
    N=len(a)
    k=np.arange(0,N)
    l=np.arange(0,N)
    kl=np.outer(k,l)
    W=np.exp(-2j*np.pi*kl/N)/N
   # print(kl)
   # print(W)
    return np.matmul(W,a)

#print(naive_dft([1,2,0,2]))

def FFT(a,inverse=False):
    N=len(a)
    power=math.log2(N)
    fac=-2j*np.pi
    if inverse:
        fac*=-1
    if int(power)!=power:
        raise ValueError("Vzorků musí být 2^N!")
    def _FFT(a,N):
        if N==1:
            return np.array(a[0])
        else:
           # print("N",N)
            k=np.arange(N//2)
            wNk=np.exp(fac*k/N)
            even=a[::2]#np.array([a[2*i] for i in k ])
            odd=a[1::2]#np.array([a[2*i+1] for i in k ])
         #   print(np.shape(even),np.shape(odd))
            Seven=_FFT(even,N//2)
            Sodd=_FFT(odd,N//2)
            #print("Seven",Seven,"Sodd",Sodd)
            #print("Sshapes",N//2,np.shape(even),np.shape(odd),np.shape(Seven),np.shape(Sodd))
            #input()
            return np.hstack([Seven+wNk*Sodd,Seven-wNk*Sodd])
    if inverse:
        return _FFT(a,N)
    else:
        return _FFT(a,N)/N
def FFT_2D(a,inverse=False):
    F1=np.array([FFT(an,inverse=inverse) for an in a])    
    return np.array([FFT(an,inverse=inverse) for an in F1.transpose()]).transpose()
def pass2D(fc,ft,mode="low",uc=None):
    N,M=np.shape(ft)
    Narr=np.arange(N)
    Marr=np.arange(M)
    Nmod=eq_freq(Narr)
    Mmod=eq_freq(Marr)
    
    fgrid=np.array(list(it.product(Nmod,Mmod))).reshape((N,M,2))
    fmag=np.sum(fgrid**2,axis=2)
    #return np.where(fmag>fc**2,0,1)
    if mode=="low":
        return np.where(fmag<fc**2,ft,0)
    elif mode=="high":
        return np.where(fmag>fc**2,ft,0)
    elif mode=="band":
        if uc is None:
            uc=2*fc
        return np.where((fc**2<fmag)*(fmag<uc**2),ft,0)
    elif mode=="smooth":
        return ft/(1+fmag/fc**2)
    elif mode=="smooth_r":
        return ft/(1+fc**2/fmag)
    else:
        raise ValueError(f"The mode {mode} is not defined!")


x=np.array([[1,0,2,4],[0,1,3,5]])
print(FFT_2D(x))


def cyclic_mirror(a):
    N,*M=a.shape
    if M:
        M=M[0]
        return np.array([[a[(-i)%N,-(j)%M] for j,_ in enumerate(a0) ] for i,a0 in enumerate(a)])
    else:
        return np.array([a[(-i)%N] for i,_ in enumerate(a) ])
    


def eq_freq(f):
    N=len(f)
    return np.where(f>N//2,f-N,f)
def even_part(a):
    return 0.5*(a+cyclic_mirror(a))
def odd_part(a):
    return 0.5*(a-cyclic_mirror(a))
"""
#print(FFT([1,2]))
    #def _FFT(a):
ars=[
    [1],
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]+[1,0,0,0]
    ]
for ar in ars:
    print(f"Array: {ar}, \n Naive: {naive_dft(ar)},\n FFT: {FFT(ar)}\n\n")
ar=np.array([4,7,8,2,1,6,3,5,7,9,4,5,6,1,10,15,16,17,18,19,20,21,22,4,5,11,26,5,4,7,6,9])
ar=even_part(ar)
bar=np.hstack([ar,np.zeros(len(ar))])
#plt.plot(ar,"-",bar,"-")
print(FFT(even_part(ar)),FFT(odd_part(ar)))
x=FFT(even_part(ar))
y=FFT(even_part(bar))
#xn=naive_dft(even_part(bar))
#y=FFT(even_part(bar))
plt.plot(np.arange(32),x)
plt.plot(np.arange(64)/2,y*2)
#plt.plot(np.arange(29)*32/29,xn)

#plt.plot(y)
plt.show()
ar=np.array([4,7,8,2,1,6,3,5,7,9,4,5,6,1,10,15,16,17,18,19,20,21,22,4,5,11,26,5,4,7,6,9])
ar=even_part(ar)
bar=np.hstack([ar,np.zeros(15)])
x=naive_dft(ar)
y=naive_dft(bar)
plt.plot(np.arange(len(x)),x)
plt.plot(np.arange(len(y))*len(x)/len(y),y*len(y)/len(x))
plt.show()
"""