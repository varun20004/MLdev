import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

VIDEO_FEED = 0
WIN_TITLE = "HELLO_WORLD"
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRAKING_CONFIDENCE = 0.3

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(VIDEO_FEED)

with mp_hands.Hands(
    min_detection_confidence= MIN_DETECTION_CONFIDENCE,
    min_tracking_confidence= MIN_TRAKING_CONFIDENCE
    ) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        
        results = hands.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image, hand, mp_hands.HAND_CONNECTIONS, 
                    mp_drawing.DrawingSpec(color=(0, 0, 225), thickness=2, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2),
                    )
            
        
        cv2.imshow(WIN_TITLE, image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()