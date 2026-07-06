import numpy as np
import cv2
import sys
#import cPickle as pickle
import pickle
from numpy.linalg import inv
import scipy.signal

#Program to open a video input file 'videorecord.txt' (python txt format using pickle). Then Upsampling takes place and after that the filtering. Finally the output is displayed on the screen.
#This is a framework for a simple video decoder to build.
#Gerald Schuller, April 2015
N=2

g=open('videorecord.txt', 'rb')
UCr=np.zeros(())
filt1=np.ones((N,N))/N;
filt2=scipy.signal.convolve2d(filt1,filt1)/N
while(True):
#load next frame from file f and "de-pickle" it, convert from a string back to colortransform or tensor:
    #reduced=pickle.load(f)
    #reduced1=pickle.load(g)
    Y=pickle.load(g)
    DCr=pickle.load(g)
    DCb=pickle.load(g)
    
    rows,cols=Y.shape
    output=np.zeros((rows,cols,3))
# filling color components with zeros
    UCr=np.zeros((rows,cols))
    UCb=np.zeros((rows,cols))
#Upsampling
    UCr[0::N,::N]=DCr;
    UCb[0::N,::N]=DCb;
#Filtering with a pyramidial filter
    UCrfilt=scipy.signal.convolve2d(UCr,filt2,mode='same')
    UCbfilt=scipy.signal.convolve2d(UCb,filt2,mode='same')
   
    B=(1*Y+1.7731*UCrfilt+0*UCbfilt);        
    G=(1*Y-0.3443*UCrfilt-0.7144*UCbfilt);
    R=(1*Y-0*UCrfilt+1.4025*UCbfilt);

    output[:,:,0]=R
    output[:,:,1]=G
    output[:,:,2]=B
  
    framedec=output.copy() 
    cv2.imshow('Video',framedec/255)
    #Wait for key for 50ms, to get about 20 frames per second playback 
    #(depends also on speed of the machine, and recording frame rate, try out):
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
