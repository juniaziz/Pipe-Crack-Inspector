import cv2
import numpy as np
import math
img = cv2.imread('hairline-crack-wall.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,200,400,apertureSize = 3)
#print len(edges)
#print len(edges[0])
#cv2.imshow('edges',edges)
#cv2.waitKey(0)
im2,contours,hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print len(contours)
print edges[1]
#print contours[88]
stuff=[]
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
    #print [(minx,maxy),(maxx,miny)]
    #print edges[miny][minx]
    #print edges[maxy][minx]
    out=np.polyfit(listx,listy,4,full=True)
    #xdiff=max(listx)-min(listx)
    #length=math.sqrt((xdiff)**2 +(out[0][0]*xdiff)**2)
    #print length
    ratio=out[1]/len(contours[i])
    if ratio<1:
        r=0
        b=0
        g=255
    elif ratio< 100:
        r=0
        b=255
        g=0
    else:
        r=255
        b=0
        g=0
    cv2.rectangle(img,(minx,maxy),(maxx,miny),(0,255,0),1)
    #cv2.line(img,(minx, int(out[0][0]*minx+out[0][1])),(maxx, int(out[0][0]*maxx+out[0][1])),(0,255,0),1)
    stuff.append(ratio)
    #cv2.drawContours(img, [contours[i]], -1, (b,g,r), 1)
#print stuff
cv2.imshow('rect', img)
cv2.waitKey(0)



#minLineLength = 30
#maxLineGap = 6
#lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
#for x in range(0, len(lines)):
#    for x1,y1,x2,y2 in lines[x]:
#        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

#cv2.imshow('hough',img)
#cv2.waitKey(0)
