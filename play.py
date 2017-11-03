from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import math

sdfactor=12
#meanfactor=3.82
meanfactor=3.2
def thresholds(bwimage):
    mean=int(np.mean(bwimage))
    sd=int(np.std(bwimage))
    lowth=sd*sdfactor
    highth=mean*meanfactor
    return lowth, highth

def gettheta(points,center):
    angles=[]
    for p in points:
        angles.append((int(math.atan2((p[1]-center[1]),(p[0]-center[0]))*57.3)))
    return angles
    
def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    
def cracksinregion(radius, allcracks, Xcentre, Ycentre):
    i=0
    while i < len(allcracks):
        j=0
        while j<len(allcracks[i]):
            rsquare=((allcracks[i][j][0][0]-Xcentre)**2)+((allcracks[i][j][0][1]-Ycentre)**2)
            if rsquare>radius**2 or rsquare<(0.92*radius)**2 :
                allcracks[i]=np.delete(allcracks[i],j,0)
            else:
                j=j+1
        if j==0:
            allcracks=np.delete(allcracks,i,0)
        else:
            i=i+1
    return allcracks

def snip(image, cracks, indices):
    x_max=0
    y_max=0
    x_min=10000
    y_min=10000
    i=0
    while i <len(cracks):
        temp_x_max=max([a[0][0] for a in cracks[i]])
        if x_max<temp_x_max:
            x_max=temp_x_max
        temp_x_min=min([a[0][0] for a in cracks[i]])
        if x_min>temp_x_min:
            x_min=temp_x_min
        temp_y_max=max([a[0][1] for a in cracks[i]])
        if y_max<temp_y_max:
            y_max=temp_y_max
        temp_y_min=min([a[0][1] for a in cracks[i]])
        if y_min>temp_x_min:
            y_min=temp_y_min
        i=i+1
    snipet=image[y_min:y_max, x_min:x_max]
    return snipet

start=time.time()
framestot=0
text_file= open('snips/coords.txt','w')
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
        edges = cv2.Canny(gray,low,high,apertureSize = 3)
        cracks=[]
        centre=len(img[0])/2, len(img)/2
        Radius=len(img)/2
        im2,contours,hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0,len(contours)):
            listx=[]
            listy=[]
            for j in range(0,len(contours[i])):
                listx.append(contours[i][j][0][0])
                listy.append(contours[i][j][0][1])
            out=np.polyfit(listx,listy,1,full=True)
            if not out[1]:
                ratio=0
            else:   
                ratio=math.sqrt(out[1])/(len(contours[i])**1.4)
            if ratio<0.2 and ratio>0.05 and len(contours[i])>15:
                cracks.append(contours[i]) 
        cracksofinterest=cracksinregion(Radius,cracks,centre[0],centre[1])
        #print len(cracksofinterest)       
        
        mids=[]
        lengths=[]
        for i in range(0,len(cracksofinterest)):     
            x=0
            y=0
            l=len(cracksofinterest[i])
            lengths.append(l)
            for j in range(0,l):
                x=cracksofinterest[i][j][0][0]+x
                y=cracksofinterest[i][j][0][1]+y
            mids.append((x/l, y/l)) 
        i=0
        sets=[]
        setstemp=[0]
        cracknum=0   
        #print mids
        while i <len(mids)-1:
            if cracknum not in setstemp:
                setstemp.append(cracknum)
            if distance(mids[i],mids[i+1])<12:
                mids[i]=((mids[i][0]*lengths[i]+mids[i+1][0]*lengths[i+1])/(lengths[i]+lengths[i+1])
                        ,(mids[i][1]*lengths[i]+mids[i+1][1]*lengths[i+1])/(lengths[i]+lengths[i+1]))
                mids=np.delete(mids,i+1,0)
                lengths=np.delete(lengths,i+1,0)
                cracknum=cracknum+1
                setstemp.append(cracknum)
            else:
                i=i+1
                sets.append(setstemp)
                setstemp=[]
                cracknum=cracknum+1
                setstemp.append(cracknum)
        sets.append(setstemp)
        
        #print mids
        theta=gettheta(mids,centre)
        #print sets
        cv2.circle(img, centre, Radius, (200,200,200))
        cv2.circle(img, centre, int(Radius*0.92), (200,200,200))
        #img = img[0:550, 0:727]
        #if len(cracksofinterest)>0:
         #   snippet=snip(img, cracksofinterest, sets[0])
          #  cv2.imwrite('snips/snip'+str(framestot)+'.jpg', snippet)
           # text_file.write('('+str(framestot)+','+str(theta[0])+')\n')
        cv2.drawContours(img, cracksofinterest, -1, (0,255,0), 1)
        for i in range(0,len(mids)):
            cv2.circle(img ,tuple(mids[i]),3,(0,0,255))
        #print stuff\par
        cv2.imshow('rect', img)
            # show the frame
        framestot=framestot+1
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break 
text_file.close()
duration=time.time()-start
print duration
print framestot
 

