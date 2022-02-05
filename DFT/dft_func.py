import numpy as np
import matplotlib.pyplot as plt
import dft
npow=7
N=2**npow
lim=1
T=2*lim
grid=np.linspace(-lim,lim,N)
#grid = np.r_[np.linspace(0, 5,N//2 ), np.linspace(-5, 0, N//2)]
dt=T/N
fgrid=np.linspace(-1/dt/2,1/dt/2,N)

df=1/T


gauss=np.exp(-np.pi*grid**2)
#rgauss=gauss
rgauss=np.roll(gauss,N//2)
fftgauss=T*dft.FFT(rgauss)
print(np.sum( (fftgauss.imag)**2))
plt.plot(grid,np.roll(rgauss,-N//2))
plt.plot(fgrid,np.roll(fftgauss.real,-N//2))
plt.show()