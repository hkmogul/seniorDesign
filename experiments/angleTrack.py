''' track the tips of both sticks '''

import numpy as np
import cv2


import sys
sys.path.append('../libraries')
# sys.path.append('libraries')
import config
import imageFunctions as img

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    xR,yR,ptsR, maskR = img.findCenter(frame, config.tipR_lower, config.tipR_upper, verbose = True)
    xL,yL,ptsL, maskL = img.findCenter(frame, config.tipL_lower, config.tipL_upper, verbose = True)
    xR2,yR2,ptsR2, maskR2 = img.findCenter(frame, config.stickR_lower, config.stickR_upper, verbose = True)
    # print "{0} {1}".format(xR2, yR2)
    xL2,yL2,ptsL2, maskL2 = img.findCenter(frame, config.stickL_lower, config.stickL_upper, verbose = True)
    mask = cv2.bitwise_or(maskR, maskL)
    mask = cv2.bitwise_or(mask, maskR2)
    mask = cv2.bitwise_or(mask, maskL2)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # cv2.imshow('mask', mask)
    
    if not img.isNan(xR) and ptsR > 500:
        print "First Location: X: {0}, Y: {1}".format(xR, yR)
        frame[yR][xR] = np.array((255,0,0))
        res[yR][xR] = np.array((255,0,0))

    if not img.isNan(xL) and ptsL > 150:
        print "Second Location: X: {0}, Y: {1}".format(xL, yL)
    else:
        print ptsL
    cv2.imshow('frame',res)
    cv2.imshow('image', frame)
    if not img.isNan(xR) and not img.isNan(xL) and ptsR > 500 and ptsL > 500:
        print "Distance between tips: {0}".format(img.dist(xR.item(),yR.item(),xL.item(),yL.item()))
    print "Angle between sticks: {0}".format(img.stickAngle(frame))
        # print "Distance between objects: {0}".format(img.dist(xR,yR,xL,yL))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break