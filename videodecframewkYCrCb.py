import numpy as np
import cv2
import sys
#import cPickle as pickle
import pickle
from numpy.linalg import inv

#Program to open a video input file 'videorecord.txt' (python txt format using pickle) and display it on the screen.
#This is a framework for a simple video decoder to build.
#Gerald Schuller, April 2015
#N=2
f=open('videorecord.txt', 'rb')

#colortransform=np.array([[0.114,0.587,0.299],[0.4997,-0.33107,-0.16864],   [-0.081282,-0.418531,0.499813]])
#colortransforminv=inv(colortransform)
#print(np.dot(colortransform,colortransforminv))
UCr=np.zeros(())
while(True):
#load next frame from file f and "de-pickle" it, convert from a string back to colortransform or tensor:
    #reduced=pickle.load(f)
    #reduced1=pickle.load(g)
    Y=pickle.load(f)
    Cb=pickle.load(f)
    Cr=pickle.load(f)
    
    rows,cols=Y.shape
    print("rows=",rows, "colums=",cols)
    output=np.zeros((rows,cols,3))
    #UCr=np.zeros((rows,cols))
    #UCb=np.zeros((rows,cols))
    #UCr[0::N,::N]=DCr;
    #UCb[0::N,::N]=DCb;
    #reduced1=reduced1
    #print(reduced1[0,0,:])
    #colortensor=np.tensordot(reduced1,colortransform,axes=1)/255
    
    #output=np.tensordot(reduced1,colortransforminv,axes=1)
    #print(output[0,0,:])
           
    R=(1*Y-0*Cb+1.4025*Cr);
    G=(1*Y-0.3443*Cb-0.7144*Cr);
    B=(1*Y+1.7731*Cb+0*Cr); 
    
    output[:,:,0]=R
    output[:,:,1]=G
    output[:,:,2]=B
    #here goes the decoding:
    framedec=output.copy() 
    print(framedec[0,0,:])
    cv2.imshow('Video',framedec/255)
    #Wait for key for 50ms, to get about 20 frames per second playback 
    #(depends also on speed of the machine, and recording frame rate, try out):
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
