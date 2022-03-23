import cv2
import sys
import mediapipe as mp
import time
s=0
if len(sys.argv) > 1:
    s = sys.argv[1]

class Handdetector():
    def __init__(self,mode=False,MaxHands=2, detectioncon=0.5,trackcon=0.5 ):
        self.mode = mode
        self.MaxHands=MaxHands
        self.detectioncon=detectioncon
        self.trackcon=trackcon
        self.mpHands = mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.MaxHands,self.detectioncon,self.trackcon)
        self.mpDraw= mp.solutions.drawing_utils

    def findhands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        self.results= self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findpos(self,img,handno=0,draw=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y *h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        return lmlist

    

def main():
    cTime=0
    pTime=0
    source=cv2.VideoCapture(s)
    detector= Handdetector()
    while cv2.waitKey(1) != 27:
        _ , img= source.read()
        img=detector.findhands(img)
        lmlist=detector.findpos(img)
        if len(lmlist)!=0:
            print(lmlist[4])
        cTime=time.time()
        fps= 1/(cTime-pTime)
        pTime= cTime
        cv2.putText(img , str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("image",img)
        

if __name__ == "__main__":
    main()