# i pro 2n-1=299  (n=150) je krásně vidět Gibbsův jev - na krajích pravoúhelníku je aproximace extrémně rozkmitaná a hodně nepřesná

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import itertools as it
def rectangle(grid,L):
    return np.where((grid+L/2)%(2*L)<L,1/L,0)
def rectFour(grid,L):
    c=it.count()
    yield 1/(2*L)*np.ones(np.shape(grid))
    next(c)
    sign=1
    for n in c:
        yield 2/(np.pi*L)*sign/(2*n-1)*np.cos(np.pi*(2*n-1)*grid/L)
        sign*=-1
def triFour(grid,L):
    c=it.count()
    yield 1/(2*L)*np.ones(np.shape(grid))
    next(c)
    
    for n in c:
        nodd=2*n-1
        yield 4/(np.pi**2*L*nodd**2)*np.cos(np.pi*(nodd)*grid/L)
def triangle(grid,L):
    modgrid=np.mod(grid+L,2*L)-L
    return 1/L*(1-np.abs(modgrid)/L)

fs = 44100
tmax=2
f0=100

L=L=1/(2*f0) #T=1/440 s => f=440 Hz. Mělo by odpovídat komornímu a, kdyby to byla harmonická vlna

grid=np.linspace(0,tmax,fs*tmax)
partialsums=[]
psum=0
nmax=100

for n,coef in enumerate(rectFour(grid,L)):
    psum+=coef
    partialsums.append(np.array(psum))
    if n==nmax:
        break
rect=rectangle(grid,L)


T=1/f0
sounds=[1/L*np.cos(f0*2*np.pi*grid),rect]+partialsums[-1:]
zoom=fs*tmax//50
#plt.ion()
for sound in sounds:
    plt.plot(grid[:zoom],sound[:zoom])
    
plt.show()
plt.pause(0.001)
#for sound in sounds: //uncomment at your own peril
#    sd.play(sound, fs,blocking=True)


tr=triangle(grid,L)
psum=0
nmax=20
partialsums=[]
for n,coef in enumerate(triFour(grid,L)):
    psum+=coef
    partialsums.append(np.array(psum))
    if n==nmax:
        break

sounds=[tr]+partialsums
for sound in sounds:
    plt.plot(grid[:zoom],sound[:zoom])

#plt.ion()

plt.show()

plt.pause(0.0001)
#for sound in sounds:
#    sd.play(sound, fs,blocking=True)
