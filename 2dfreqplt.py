#3D plot of 2D frequency response
#Gerald Schuller, May 2015

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import scipy.signal

#A=np.random.rand(4,4)
filt1=np.ones((8,8))
filt2=scipy.signal.convolve2d(filt1,filt1)/8

A=np.abs(np.fft.fft2(filt2,(32,32)));

[r,c]=A.shape
x=range(c)
y=range(r)
X,Y=np.meshgrid(x,y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(X,Y,A)
ax.plot_wireframe(X,Y,A)
#plt.imshow(A,cmap='gray')

ax.set_xlabel('k_2')
ax.set_ylabel('k_1')
ax.set_zlabel('Value')
plt.title('2D frequency response of pyramidal filter kernel with size 32 FFT')
plt.show()


