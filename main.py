import cv2
from hand_utilities import Hand
from arduino_connect import ArduinoConnection
import math


# connect to Arduino
ard_device = ArduinoConnection("COM4", 9600)
# connect to camera
cap = cv2.VideoCapture(0)
hand = Hand()
print(Hand.fingers_ids)
while True:
    ret, frame = cap.read()

    frame1 = cv2.resize(frame, (320, 240))
    print(type(frame1))
    states_fingers = hand.get_fingers_state(frame1)
    if states_fingers:
        values = list()
        for id_finger in hand.fingers_ids:
            values.append(states_fingers[id_finger])
        # send finger states to Arduino
        ard_device.write_array([3, *values])
    print(states_fingers)
    cv2.imshow("Frame", frame1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
