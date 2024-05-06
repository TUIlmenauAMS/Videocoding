#Program to capture a video from the default camera (0), compute the 2D FFT 
#on the Green component, take the magnitude (phase) and display it live on the screen
#Gerald Schuller, Nov. 2014
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    [retval, frame] = cap.read()    
    #compute magnitude of 2D FFT of green component 
    #with suitable normalization for the display:
    frame=np.abs(np.fft.fft2(frame[:,:,1]/255.0))/512.0
    #angle/phase:
    #frame=(3.14+np.angle(np.fft.fft2(frame[:,:,1]/255.0)))/6.28
    # Display the resulting frame
    cv2.imshow('2D FFT Betrag des Videos',frame)
    #Keep window open until key 'q' is pressed:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
