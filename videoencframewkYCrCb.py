import numpy as np
import cv2
import cPickle as pickle

#Program to capture video from a camera and store it in an recording file, in Python txt format, using cPickle
#This is a framework for a simple video encoder to build.
#It writes into file 'videorecord.txt'
#Gerald Schuller, April 2015

cap = cv2.VideoCapture(0)
#N=2
f=open('videorecord.txt', 'w')

#Process 25 frames:
for n in range(25):

    ret, frame = cap.read()
    [rows,columns,c]=frame.shape
    #Ds=np.zeros((rows/N,columns/N));
    #colortensor=np.zeros((rows,columns,c))
    colortransform=np.array([[0.114,0.587,0.299],[0.4997,-0.33107,-0.16864],   [-0.081282,-0.418531,0.499813]])
    if ret==True:
       
        #Here goes the processing to reduce data... 
        reduced = np.zeros((rows,columns,c))
        #print(reduced[0,0,:])
        #colortensor=np.tensordot(reduced,colortransform.T,axes=1)
        #print(colortensor[0,0,:])
        #colortensor=np.array(colortensor,dtype='uint8')
        Y=(0.114*frame[:,:,0]+0.587*frame[:,:,1]+0.299*frame[:,:,2]);        
        
        Cb=(0.4997*frame[:,:,0]-0.33107*frame[:,:,1]-0.16864*frame[:,:,2]);
    #V=R-Y:
        Cr=(-0.081282*frame[:,:,0]-0.418531*frame[:,:,1]+0.499813*frame[:,:,2]);
        #reduced[:,:,0]=Y
        #reduced[:,:,1]=Cb
        #reduced[:,:,2]=Cr
        
        #show frames:
        cv2.imshow('Original',frame)
    	# cv2.imshow('Luminanz Y',Y/255)
    	# cv2.imshow('Farbkomponente U',np.abs(Cr))
    	#cv2.imshow('Farbkomponente V',np.abs(Cb))
        #"Serialize" the captured video frame (convert it to a string) 
        #using pickle, and write/append it to file f:
      #  pickle.dump(Ds,f)
	#print(np.abs(U[0,0]))
        #pickle.dump(reduced,g)
        #print(Cb[0,0])
        Y=np.array(Y, dtype='uint8')
        Cr=np.array(Cr, dtype='int8')
        Cb=np.array(Cb, dtype='int8')
        #DCr=Cr[0::N,::N];
	#DCb=Cb[0::N,::N];
        #print(Cb[0,0])
        pickle.dump(Y,f)
        pickle.dump(Cb,f)
        pickle.dump(Cr,f)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
f.close()
cv2.destroyAllWindows()
