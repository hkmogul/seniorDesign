''' track the tips of both sticks '''

import numpy as np
import cv2

import config
import imageFunctions as img

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    xR,yR,ptsR, maskR = img.findCenter(frame, config.tipR_lower, config.tipR_upper, verbose = True)
    xL,yL,ptsL, maskL = img.findCenter(frame, config.tipL_lower, config.tipL_upper, verbose = True)
    mask = cv2.bitwise_or(maskR, maskL)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    # cv2.imshow('mask', mask)
    cv2.imshow('frame',res)
    if not img.isNan(xR) and ptsR > 500:
        print "First Location: X: {0}, Y: {1}".format(xR, yR)
    if not img.isNan(xL) and ptsL > 500:
        print "Second Location: X: {0}, Y: {1}".format(xL, yL)

    if not img.isNan(xR) and not img.isNan(xL) and ptsR > 500 and ptsL > 500:
        print "Distance between objects: {0}".format(img.dist(xR.item(),yR.item(),xL.item(),yL.item()))
        # print "Distance between objects: {0}".format(img.dist(xR,yR,xL,yL))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
