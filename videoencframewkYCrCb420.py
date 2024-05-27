import numpy as np
import cv2
#import cPickle as pickle
import pickle
import scipy.signal

#Program to capture video from a camera and store it in an recording file, in Python txt format, using cPickle
# Also, filed is divided into luminance and two color components. By using 4:2:0 scheme, color components are then downsampled by the factor of 2. To reduce aliasing artifacts pyramidial filter is used.
#This is a framework for a simple video encoder to build.
#It writes into file 'videorecord.txt'
#Gerald Schuller, April 2015

cap = cv2.VideoCapture(0)
N=2
g=open('videorecord.txt', 'wb')
# filter is created by convolving two rectangular filters
#Triangular filter kernel:
filt1=np.ones((N,N))/N;
filt2=scipy.signal.convolve2d(filt1,filt1)/N
#Process 25 frames:
for n in range(25):

    ret, frame = cap.read()
    [rows,columns,c]=frame.shape
 
    if ret==True:
       
        #Here goes the processing to reduce data... 
        reduced = np.zeros((rows,columns,c))
        Y=(0.114*frame[:,:,0]+0.587*frame[:,:,1]+0.299*frame[:,:,2]);        
        
        Cb=(0.4997*frame[:,:,0]-0.33107*frame[:,:,1]-0.16864*frame[:,:,2]);
   
        Cr=(-0.081282*frame[:,:,0]-0.418531*frame[:,:,1]+0.499813*frame[:,:,2]);
        reduced[:,:,0]=Y
        reduced[:,:,1]=Cb
        reduced[:,:,2]=Cr
       
        cv2.imshow('Original',frame)
        #cv2.imshow('Luminanz Y',Y/255)
        #cv2.imshow('Unterabgetastetes Y',Ds)
        #cv2.imshow('Farbkomponente U',np.abs(Cr))
        #cv2.imshow('Farbkomponente V',np.abs(Cb))
       
   
        #Two color components are filtered first
        Crfilt=scipy.signal.convolve2d(Cr,filt2,mode='same')
        Cbfilt=scipy.signal.convolve2d(Cb,filt2,mode='same')

        # Downsampling
        DCr=Crfilt[0::N,::N];
        DCb=Cbfilt[0::N,::N];
        #cv2.imshow('Crfiltered',DCr)
        #cv2.imshow('Cbfiltered',DCb)
   
        Y=np.array(Y, dtype='uint8')
        DCr=np.array(DCr, dtype='int8')
        DCb=np.array(DCb, dtype='int8')
        #"Serialize" the captured video frame (convert it to a string) 
        #using pickle, and write/append it to file g:
        pickle.dump(Y,g)
        pickle.dump(DCr,g)
        pickle.dump(DCb,g)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
g.close()
cv2.destroyAllWindows()
