#3D plot example
#Gerald Schuller, April 2015

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import scipy.signal

#A=np.random.rand(4,4)
filt1=np.ones((8,8))
filt2=scipy.signal.convolve2d(filt1,filt1)/8
A=filt2;

[r,c]=A.shape
x=range(c)
y=range(r)
X,Y=np.meshgrid(x,y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(X,Y,A)
ax.plot_wireframe(X,Y,A)
#plt.imshow(A,cmap='gray')

ax.set_xlabel('n_2')
ax.set_ylabel('n_1')
ax.set_zlabel('Value')
plt.title('Pyramindal 2D filter impulse response')
plt.show()


