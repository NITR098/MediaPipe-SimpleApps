import cv2
import numpy as np
import HandModule as hm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# define colors
blue = [255, 0, 0]
green = [0, 255, 0]
red = [0, 0, 255]
purple = [255, 0, 255]
# read volume image
vol_img = cv2.imread('./volume.jfif')
vol_img = cv2.resize(vol_img, (40, 40))

# activate webcam and change webcam frame size
width, height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get speakers info with pycaw module
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


volRange = volume.GetVolumeRange()
minvol = volRange[0]
maxvol = volRange[1]

detector = hm.Detector(detectionCon = 0.75)

vol_percentage = 0
vol_bar = 400

while True:
    _, frame = cap.read()
    frame[400:440, 50:90] = vol_img
    frame = detector.findHands(frame, draw = True)
    landmarkList = detector.landmarkPosition(frame, draw = False)
    if len(landmarkList) != 0:
        #print(landmarkList[4], landmarkList[8])
        x1, y1 = landmarkList[4][1], landmarkList[4][2]
        x2, y2 = landmarkList[8][1], landmarkList[8][2]
        xcenter, ycenter = (x1 + x2)//2,(y1 + y2)//2
        cv2.circle(frame, (x1, y1), 10, purple, -1)
        cv2.circle(frame, (x2, y2), 10, purple, -1)
        cv2.line(frame, (x1, y1), (x2, y2), green, 3)
        cv2.circle(frame, (xcenter, ycenter), 10, purple, -1)
        len_index2thumb = np.hypot(x2 - x1, y2 - y1)
        #print(len_index2thumb) # 15 - 215
        if len_index2thumb < 20:
            cv2.circle(frame, (xcenter, ycenter), 10, green, -1)
        if len_index2thumb > 200:
            cv2.circle(frame, (xcenter, ycenter), 10, red, -1)
            
        vol = np.interp(len_index2thumb, [15, 215], [minvol, maxvol])
        vol_percentage = np.interp(len_index2thumb, [15, 215], [0, 100])
        vol_bar = np.interp(len_index2thumb , [15 , 215] , [420 , 180])
        volume.SetMasterVolumeLevel(vol, None)
    
    cv2.putText(frame, f'{int(vol_percentage)} %', (70, 465), cv2.FONT_HERSHEY_COMPLEX,
                1, green, 3)
    bar_interval = int(np.interp(vol_bar, [180, 420], [5, 0]))
    print(bar_interval)
    for i in range(0, bar_interval):
        x1 = int(95 + 10*i)
        y1 = int(400 - 20*i)
        x2 = int(100 + 10*i)
        y2 = 440
        cv2.rectangle(frame , (x1,y1) , (x2 , y2) , green , -1)
    cv2.imshow('Volume Control', frame)
    cv2.waitKey(1)
    