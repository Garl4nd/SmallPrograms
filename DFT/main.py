#Produces filtered (band-passed, low-passed, high-passed) version of a base image 
import dft
from  PIL import Image

import numpy as np
import matplotlib.pyplot as plt
im=np.array(Image.open("fig.png"))
skip=0
step=2**skip
N=512//step
im=np.array([[np.sum(im[i*step:(i+1)*step,j*step:(j+1)*step]) for j in range(N)] for i in range(N)])
#im=im[:512:2**skip,:512:2**skip,0]

#plt.imshow(im)
ft=dft.FFT_2D(im)
herm=dft.cyclic_mirror(ft)
#print(ft[4,5],ft[N-4,N-5])
"""for i in range(1,N):
    for j in range(1,N):
        if ft[i,j]!=herm[i,j]:#ft[N-i,N-j]:
            print("rovna se",i,j,ft[i,j],herm[i,j])
"""
summed=ft+herm
#print(summed.imag)
#print(np.sum( (summed.imag)**2))
#ft=np.fft.fft2(im)
herm=np.conj(dft.cyclic_mirror(ft))
#print(ft==herm)

#lft=dft.pass2D(32,ft,mode="low")
#uft=dft.pass2D(32,ft,mode="high")
#bft=dft.pass2D(16,ft,mode="band")
#sft=dft.pass2D(32,ft,mode="smooth")

#lft=dft.FFT_2D(lft,inverse=True)
#uft=dft.FFT_2D(uft,inverse=True)
#bft=dft.FFT_2D(bft,inverse=True)
#uft=dft.FFT_2D(dft.pass2D(32,ft,mode="low"),inverse=True)
#uft=dft.FFT_2D(dft.pass2D(32,ft,mode="high"),inverse=True)
#sfts=[dft.FFT_2D(dft.pass2D(fc,ft,mode="smooth_r"),inverse=True) for fc in [1,2,4,8,16,32,64,128]]
sfts=[dft.FFT_2D(dft.pass2D(fc,ft,mode="low"),inverse=True) for fc in [1,2,4,8,16,32,64,128]]

print("imag",np.sum( (summed.imag)**2))
for picture in sfts+[]:#(im,lft,sft,uft,bft):
    fig,_=plt.subplots()
    img=plt.imshow(picture.real)
    plt.colorbar(img)

#plt.plot(lft)
plt.show()