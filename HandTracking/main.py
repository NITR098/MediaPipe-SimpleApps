'''
Tracking hand with its landmarks
'''

import cv2
import mediapipe as mp

red = [0, 0, 255]
green = [0, 255, 0]
blue = [255, 0, 0]

mediapipeHands = mp.solutions.hands
hands = mediapipeHands.Hands()
Draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handlandmarks in results.multi_hand_landmarks:
            Draw.draw_landmarks(frame, handlandmarks, mediapipeHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handlandmarks.landmark):
                height, width, _ = frame.shape
                x, y = int(lm.x*width), int(lm.y*height)
                print(id, x, y)
                if id == 4:
                    cv2.circle(frame, (x, y), 15, blue, -1)
                #cv2.circle(frame, (x, y), 15, blue, -1)


    cv2.imshow('WebCam', frame)
    cv2.waitKey(1)

