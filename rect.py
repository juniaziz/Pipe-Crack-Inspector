from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import math

sdfactor=18
#meanfactor=3.82
meanfactor=6
def thresholds(bwimage):
    mean=int(np.mean(bwimage))
    sd=int(np.std(bwimage))
    lowth=sd*sdfactor
    highth=mean*meanfactor
    return lowth, highth
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	img = frame.array

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        low,high=thresholds(gray)
        edges = cv2.Canny(gray,200,400,apertureSize = 3)
        im2,contours,hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


        for i in range(0,len(contours)):
            listx=[]
            listy=[]
            maxx=0
            maxy=0
            minx=10000
            miny=10000
            for j in range(0,len(contours[i])):
                listx.append(contours[i][j][0][0])
                listy.append(contours[i][j][0][1])
                if contours[i][j][0][0]>maxx:
                    maxx=contours[i][j][0][0]
                if contours[i][j][0][1]>maxy:
                    maxy=contours[i][j][0][1]
                if contours[i][j][0][0]<minx:
                    minx=contours[i][j][0][0]
                if contours[i][j][0][1]<miny:
                    miny=contours[i][j][0][1]
        
            out=np.polyfit(listx,listy,1,full=True)
        
            if not out[1]:
                ratio=0
            else:   
                ratio=math.sqrt(out[1])/(len(contours[i])**1.4)
            if ratio>0.5 and len(contours[i])>35:
                r=0
                b=255
                g=0
                #print ratio\par
                #print out[1]\par
                #print len(contours[i])\par
            elif ratio< 0.5 and len(contours[i])>35:
                r=0
                b=0
                g=255
                
                #print ratio\par
                
            else:
                r=0
                b=0
                g=255
                #print ratio\par
            #cv2.rectangle(img,(minx,maxy),(maxx,miny),(0,255,0),1)\par
            #cv2.line(img,(minx, int(out[0][0]*minx+out[0][1])),(maxx, int(out[0][0]*maxx+out[0][1])),(0,255,0),1)\par
            
            cv2.drawContours(img, [contours[i]], -1, (b,g,r), 1)
        #print stuff\par
        cv2.imshow('rect', img)
            # show the frame
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break 
     
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 

