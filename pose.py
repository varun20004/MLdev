import cv2
import mediapipe as mp
import sys
import time
s=0
if len(sys.argv) >1:
    s=sys.argv[1]
mppose=mp.solutions.pose
pose=mppose.Pose()
source = cv2.VideoCapture(s)
mpDraw= mp.solutions.drawing_utils
cTime= 0
pTime=0
while cv2.waitKey(1) !=27:
    _ , img =source.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
  
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mppose.POSE_CONNECTIONS)
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h, w,c =img.shape
            print(id,lm)
            cx,cy=int(lm.x*w) , int(lm.y*h)
            cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)

    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)