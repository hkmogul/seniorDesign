''' Copied code for tracking colored objects.  Will start with the straw of my cup '''

import cv2
import numpy as np


def findPosition(mask):
    points = np.where(mask)
    return np.mean(points[0]), np.mean(points[1])



cap = cv2.VideoCapture(0)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.namedWindow('res', cv2.WINDOW_NORMAL)
while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of orange color in HSV
    lower_orange = np.array([7,175,175])
    upper_orange = np.array([15,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    # cv2.resizeWindow('frame', 500,500)
    cv2.imshow('mask',mask)
    # cv2.resizeWindow('mask', 500,500)
    y, x = findPosition(mask)
    print "X: {0}, Y: {1}".format(x, y)
    cv2.imshow('res',res)
    # cv2.resizeWindow('res', 500,500)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
