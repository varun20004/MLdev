import cv2
import time
import numpy as np
import sys
import handmodule as htm
import math
from subprocess import call
s=0
if len(sys.argv) > 1:
    s = sys.argv[1]
wcam,hcam=640,480
source=cv2.VideoCapture(s)
source.set(3,wcam)
source.set(4,hcam)
cTime=0
pTime=0
vol=0
volbar=400
detector=htm.Handdetector()
while cv2.waitKey(1) !=27:
    _,img=source.read()
    img=detector.findhands(img)
    lmlist=detector.findpos(img,draw=False)
    if len(lmlist)!=0:
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        valid = False
        vol=np.interp(length,[50,300],[0,100])
        volbar=np.interp(length,[50,300],[400,150])
        print(vol)
        while not valid:
            volume =vol

            try:
                volume = int(volume)

                if (volume <= 100) and (volume >= 0):
                    call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
                    valid = True

            except ValueError:
                pass
                
        
        
        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    cv2.imshow('image',img)