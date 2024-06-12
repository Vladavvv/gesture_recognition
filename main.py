import time
import cv2
import MediapipeModule as htm
import paho.mqtt.client as mqtt
import urllib.request
import numpy as np

mqtt_broker = "broker.hivemq.com"  # mqtt broker
client = mqtt.Client("client name")  # choose your own client name
client.connect(mqtt_broker)

wCam, hCam = 640, 480

url = 'http://192.168.78.38/cam-mid.jpg'
cv2.namedWindow("live Cam", cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(url)

# cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.Handsmodule()


def convert_range(value, min1, max1, min2, max2):
    if value < min1:
        value = min1
    elif value > max1:
        value = max1

        # Apply the formula to map the value from one range to another
    new_value = ((value - min1) / (max1 - min1)) * (max2 - min2) + min2
    return new_value


while True:
    # success, img = cap.read()
    # img = detector.findHands(img)
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    # ret, frame = cap.read()
    im = cv2.imdecode(imgnp, -1)
    im_flipped = cv2.flip(im, -1)
    img = detector.searchHands(im_flipped)
    landmarkList = detector.getPosition(img)

    if len(landmarkList) != 0:
        x1, y1 = landmarkList[8][1:]
        x2, y2 = landmarkList[12][1:]

        fingers = detector.raisedFingers()
        # print(fingers)

        if fingers[1] == 1 and fingers[2] == 1 and fingers[0]+fingers[3]+fingers[4] == 0:
            length, img, lineInfo = detector.findDistanceBetweenTwoPoints(8, 12, img)
            converted_value = convert_range(length, 40, 90, 0, 255)
            client.publish("fan", int(converted_value))
            print("_______________")
            print(length)
            # print(converted_value)
            # print("_______________")


        if fingers.count(1) == 5:
            print("light")
            client.publish("light", 1)

        if fingers.count(1) == 0:
            print("light")
            client.publish("light", 0)

        totalFingers = fingers.count(1)
        # print(totalFingers)

    # cv2.imshow("Image", img)
    cv2.imshow('live Cam', im_flipped)
    cv2.waitKey(1)



