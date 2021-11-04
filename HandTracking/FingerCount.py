import cv2
import mediapipe as mp
import HandModule as hm

green = [0, 255, 0]

cap = cv2.VideoCapture(0)
detector = hm.Detector(detectionCon = 0.75)
fingers_idx = [4, 8, 12, 16, 20]

while True:
    _, frame = cap.read()
    frame = detector.findHands(frame)
    landmarkList = detector.landmarkPosition(frame, draw = False)
    #print(landmarkList)
    if len(landmarkList) != 0:
        fingers = []
        '''if landmarkList[8][2] < landmarkList[6][2]:
            print('Thumb is open.')
        else:
            print('Thumb is closed.')'''
        # 4 fingers other than Thumb
        for index in range(1, len(fingers_idx)):
            if landmarkList[fingers_idx[index]][2] <= landmarkList[fingers_idx[index] - 2][2]:
                fingers.append(0)
            else:
                fingers.append(1)
        # Thumb
        if landmarkList[fingers_idx[0]][1] >= landmarkList[fingers_idx[0] - 2][1]:
            fingers.insert(0, 0)
        else:
            fingers.insert(0, 1)
        number_of_fingers = fingers.count(0)
        print(number_of_fingers)
        #print(fingers)
        cv2.putText(frame, str(number_of_fingers), (50, 100), cv2.FONT_HERSHEY_PLAIN, 8, green, 7)
    cv2.imshow('Finger Counter', frame)
    cv2.waitKey(1)
