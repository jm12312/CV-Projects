import mediapipe as mp
import cv2
import HandTrackingModule as htm
import time
import imutils
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 640)
detector = htm.handDetector(detectionCon=0.9)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""
keyboard = Controller()
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (96, 96, 96), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    return img

class Button():
    def __init__(self, pos, text, size=[80, 80]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([110 * j + 5, 110 * i + 50], key))


#myButton = Button([10, 50], "Q")

while True:
    success, img = cap.read()
    img = imutils.resize(img, 1200, 480)
    img = detector.findHands(img)
    lmlist, bboxinfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
    #img = myButton.draw(img)

    if lmlist:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmlist[8][1] < x + w and y < lmlist[8][2] < y + h:
                #print("Here")
                cv2.rectangle(img, button.pos, (x + w, y + h), (64, 64, 64), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                lf = detector.fingersUp()
                if lf[4]:
                    keyboard.press(Key.backspace)
                    time.sleep(0.15)
                #print(l)

                if l< 40:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                    finalText += button.text
                    time.sleep(0.2)
    #cv2.rectangle(img, (50, 450), (700, 550), (175, 0, 175), cv2.FILLED)
    #cv2.putText(img, finalText, (60, 525), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    # quits the program using 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


"""""
    a, _, _ = detector.findDistance(4, 16, img, draw=False)
                print(a)
                if a < 30:
                    keyboard.press(Key.backspace)
                    time.sleep(0.15)
"""
