import cv2
import numpy as np
import math
import sys
sys.setrecursionlimit(2000)
def isWhite(pixel):
    if pixel==0:
        return False
    else:
        return True

def singleFeature(x,y,xlimit,ylimit,line):
    for i in range(x-3, x+3):
            if i<0 or i>xlimit-1:
                   continue
            for j in range(y-3, y+3):
                if j<0 or j>ylimit-1 or (i,j) in line:
                   continue
                if isWhite(edges[j][i]):
                    line.append((i,j))
                    singleFeature(i,j,xlimit,ylimit,line)
    return

img = cv2.imread('hairline-crack-wall.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,400,800,apertureSize = 3)
features=[]
ylimit=len(edges)
xlimit=len(edges[0])
for y in range(0,ylimit):
    for x in range(0, xlimit):
        for feature in features:
            if (x,y) in feature:
                break
        line=[(x,y)]
        singleFeature(x,y,xlimit,ylimit,line)
        features.append(line)

print len(features)

for i in range(0,len(features)):
    listx=[]
    listy=[]
    maxx=0
    maxy=0
    minx=10000
    miny=10000
    for j in range(0,len(features[i])):
        listx.append(features[i][j][0])
        listy.append(features[i][j][1])
        if features[i][j][0]>maxx:
            maxx=features[i][j][0][0]
        if features[i][j][1]>maxy:
            maxy=features[i][j][1]
        if features[i][j][0]<minx:
            minx=features[i][j][0][0]
        if features[i][j][1]<miny:
            miny=features[i][j][1]
    out=np.polyfit(listx,listy,4,full=True)
    ratio=out[1]/len(features[i])
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
    #stuff.append(ratio)
    #cv2.drawContours(img, [contours[i]], -1, (b,g,r), 1)
cv2.imshow('rect', img)
cv2.waitKey(0)
        
        
                   
                   

        
