import numpy as np
import cv2
import sys
#import cPickle as pickle
import pickle
from numpy.linalg import inv
import scipy.signal

#Program to open a video input file 'videorecord.txt' (python txt format using pickle). Then Upsampling takes place and after that the filtering. Finally the output is displayed on the screen.
#And with motion compensated compression, transmitting every 2nd frame as I Frame, and interpolates 
#the in between frames (like P-Frames)
#Write to file instead of window.
#This is a framework for a simple video decoder to build.
#Gerald Schuller, June 2022
N=2

g=open('videorecord.txt', 'rb')
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #for writing to mp4 file



UCr=np.zeros(())
filt1=np.ones((N,N))/N;
filt2=scipy.signal.convolve2d(filt1,filt1)/N

for n in range(25):
    print("Frame no ",n)
    #every 2nd frame is an iframe:
    if n%2==0:
      iframe=True;
    else:
      iframe=False;

    if iframe: 
      print("IFrame")
      #load next frame from file f and "de-pickle" it, convert from a string back to colortransform or tensor:
      #reduced=pickle.load(f)
      #reduced1=pickle.load(g)
      Y=pickle.load(g)
      (height, width)=Y.shape
      if n==0:
         out = cv2.VideoWriter('decoded.mp4',fourcc, 20.0, (width,height)) #write to this file
      #print("Y.shape=", Y.shape)
      DCr=pickle.load(g)
      DCb=pickle.load(g)
    else:
      print("PFrame")
      MV=pickle.load(g)
      MV=MV.astype(int)
      #print(MV[0:4,0:4])

    if iframe:
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
  
      framedec=np.clip(output, 0,255) 
    else:
      print("Motion compensation across all blocks")
      #output=np.zeros((rows,cols,3))
      output=framedec.copy()
      for blockx in range(cols//8):
        for blocky in range(rows//8):
          #Output frame is shifted previous frames
          #print(output[blocky*8:blocky*8+8,blocky*8:blocky*8+8,:].shape)
          #print(MV[blocky,blockx,0])
          #print(framedec[blocky*8+MV[blocky,blockx,0]:blocky*8+MV[blocky,blockx,0]+8, blockx*8+MV[blocky,blockx,1]:blockx*8+MV[blocky,blockx,1]+8,:].shape)
          #output[blocky*8:blocky*8+8,blockx*8:blockx*8+8,:]=framedec[blocky*8+MV[blocky,blockx,0]:blocky*8+MV[blocky,blockx,0]+8, blockx*8+MV[blocky,blockx,1]:blockx*8+MV[blocky,blockx,1]+8,:]
          output[blocky*8+np.arange(8),blockx*8+np.arange(8),:]=framedec[blocky*8+MV[blocky,blockx,0]+np.arange(8), blockx*8+MV[blocky,blockx,1]+np.arange(8),:]
      framedec=output.copy() 
    #cv2.imshow('Video',framedec/255)
    framedec=np.array(framedec, dtype='uint8') #convert to uint8 for RGB
    out.write(framedec)
    #Wait for key for 50ms, to get about 20 frames per second playback 
    #(depends also on speed of the machine, and recording frame rate, try out):
    #if cv2.waitKey(50) & 0xFF == ord('q'):
    #    break

g.close()
cap.release()
cv2.destroyAllWindows()
