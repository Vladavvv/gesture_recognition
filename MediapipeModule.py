import cv2
import mediapipe as med
import time
import math


class Handsmodule():
    def __init__(self):
        self.mediapipeHands = med.solutions.hands
        self.hands = self.mediapipeHands.Hands(static_image_mode=False, max_num_hands=1, model_complexity= 1,
                                               min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.tips = [4, 8, 12, 16, 20]
        self.mediapipeDraw = med.solutions.drawing_utils


    def searchHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mediapipeDraw.draw_landmarks(img, handLms, self.mediapipeHands.HAND_CONNECTIONS)
        return img

    def raisedFingers(self):
        fingers = []

        # Thumb
        if self.landmarkList[self.tips[0]][1] > self.landmarkList[self.tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1, 5):
            if self.landmarkList[self.tips[id]][2] < self.landmarkList[self.tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers



    def findDistanceBetweenTwoPoints(self, p1, p2, img):
        x1, y1 = self.landmarkList[p1][1:]
        x2, y2 = self.landmarkList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def getPosition(self, img):
        xList = []
        yList = []
        # bbox = []
        self.landmarkList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0] ## 0 is a hand number
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.landmarkList.append([id, cx, cy])
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            # bbox = xmin, ymin, xmax, ymax

            cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 25, 0), 2)

        return self.landmarkList
