import cv2
import time
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1200, 1200
cap = cv2.VideoCapture(0)
# propid 3 : width 4:height
cap.set(3, wCam)
cap.set(4, hCam)
Ctime = 0
Ptime = 0
detector = htm.handDetector(detectionCon=0.9, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
volBar = 400
vol = 0
volPer = 0
area =0
colorVol = (255, 0, 0)
while True:
    success, img = cap.read()
    detector.findHands(img)
    lmlist, bbox = detector.findPosition(img, draw=True)
    if len(lmlist) !=0:
        #print(lmlist[4], lmlist[8])
        # Filter based on size
        area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        # area of the bounding box
        # area can be set based on distance
        if 250<= area <=1500:

            # Find distance between index and thumb
            length, img, lineinfo = detector.findDistance(4, 8, img)

            # Convert volume
            # interp: interpolation function in numpy
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])

            # Change in volume. More smoothness, better volume set
            smoothness = 5
            volPer = smoothness * round(volPer/smoothness)

            # Check if finger up returns a list [0, 0, 0, 0, 0] if none of the fingers are up
            fingers = detector.fingersUp()
            #print(fingers)

            # if pinky finger is up, set volume
            if fingers[4]:
                # Converts logarithmic scale to linear scale
                volume.SetMasterVolumeLevelScalar(volPer/100, None)
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 10, (255, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

    # Drawings
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(volPer)) + "%", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, "Vol Set " + str(int(cVol)), (400, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 2)

    # Frame rate (FPS)
    Ctime = time.time()
    fps = 1/(Ctime - Ptime)
    Ptime = Ctime
    cv2.putText(img, "FPS " + str(int(fps)), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    # Display image
    cv2.imshow("Image", img)

    # quits the program using 'q'
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
