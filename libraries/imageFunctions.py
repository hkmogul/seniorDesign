''' Utilities for processing images (such as height, angle, etc) '''

import numpy as np
import cv2
import math
import config
import os
import threading
import time
import sys

''' check if number is undefined '''
def isNan(num):
    return num != num

''' Find a position given the upper and lower hsv ranges
    Returns NaN for x, y if

'''
def findCenter(image, lower, upper, verbose = False):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    points = np.where(mask)
    if not verbose:
        return np.median(points[1]), np.median(points[0]), points[0].shape[0]
    else:
        return np.median(points[1]), np.median(points[0]), points[0].shape[0], mask


'''
Return height of point on scale (in pixels for now)
HSV = vstack of lower;upper thresholds for color to detect
return None if the color in question can't be found
'''
def getHeightRaw(image, hsvL, hsvU, scale =1):
    x, y, pts = findCenter(image, hsvL,hsvU)
    if isNan(x) or pts < config.ptsThresh:
        return -1
    else:
        return (image.shape[0]-y)*scale

def getHeights(image, scale = 1):
    right = getHeightRaw(image, config.tipR_lower, config.tipR_upper, scale = scale)
    left = getHeightRaw(image, config.tipL_lower, config.tipL_upper, scale = scale)
    return left, right
'''
Find positions of two color ranges,
calculate distance from each other
'''
def getDistance(image, hsv1, hsv2, scale =1):
    x1, y1, pts1 = findCenter(image, hsv1[0], hsv1[1])
    x2, y2, pts2 = findCenter(image, hsv2[0], hsv2[1])
    if not isNan(x1) and not isNan(x2):
        return math.sqrt((x1-x2)^2 + (y1-y2)^2)* scale
    else:
        return None
# ''' get angle of single stick.  hsv1 and hsv2 correlate to stick hsv thresholds'''
# def getAngle(image, hsv1, hsv2, right = False):
#     x1, y1, pts1 = findCenter(image, hsv1[0], hsv1[1])
#     y1 = image.shape[0]- y1
#     x2, y2, pts2 = findCenter(image, hsv2[0], hsv2[1])
#     # x2, y2 = mat2coord(image.shape, x1,y1)
#     y2 = image.shape[0]- y2

#     # print "{0}, {1}".format(x2, y2)
#     if not isNan(x1) and not isNan(x2) and min(pts1, pts2)> config.ptsThresh:

#         y1 = image.shape[0]-y1
#         y2 = image.shape[0]-y2

#         if right:
#             if x2 < x1:
#                 return math.degrees(math.atan((x1-x2)/math.fabs(y2-y1)))
#             # stick not pointed towards center in this case
#             else:
#                 return None
#         # for left stick
#         else:
#             if x2 > x1:
#                 return math.degrees(math.atan((x2-x1)/math.fabs(y2-y1)))
#             else:
#                 return None
#         # slope = (y1-y2)/(x1-x2)
#         # # print "DEBUG MODE SLOPE IS {}".format(slope)
#         # # print  math.degrees(math.atan(slope))
#         # return math.degrees(math.atan(slope))
#     else:
#         return None

def getAngle(image, stick_upper,stick_lower, tip_upper, tip_lower):
    xS, yS, ptsS = findCenter(image, stick_lower, stick_upper)
    xT, yT, ptsT = findCenter(image, tip_lower, tip_upper)
    # make vector-ish 
    dx = math.fabs(xS-xT)
    dy = math.fabs(yS-yT)

    if dy != 0:
        return math.atan(dx/dy)
    else:
        return None


''' uses config hsv bounds to find angle between 2 sticks '''
def stickAngle(image):
    # angleR = getAngle(image, np.vstack((config.stickR_lower, config.stickR_upper)), np.vstack((config.tipR_lower, config.tipR_upper)), right = True)
    # angleL = getAngle(image, np.vstack((config.stickL_lower, config.stickL_upper)), np.vstack((config.tipL_lower, config.tipL_upper)))

    angleR = getAngle(image, config.stickR_upper, config.stickR_lower, config.tipR_upper, config.tipR_lower)
    angleL = getAngle(image, config.stickL_upper, config.stickL_lower, config.tipL_upper, config.tipL_lower)
    # print angleR
    # print angleL

    if angleR is None or angleL is None:
        return None
    else:
        # print angleR+angleL
        # print vecAngle(image)
        return math.degrees(angleR+angleL)

''' uses vector geometry to find the angle between the sticks instead '''
def vecAngle(image):
    def dotproduct(v1, v2):
        return sum((a*b) for a, b in zip(v1, v2))

    def length(v):
        return math.sqrt(dotproduct(v, v))

    def angle(v1, v2):
        return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
    xRS, yRS, ptsRS = findCenter(image, config.stickR_lower, config.stickR_upper)
    xRT, yRT, ptsRT = findCenter(image, config.tipR_lower, config.tipR_upper)
    xLS, yLS, ptsLS = findCenter(image, config.stickL_lower, config.stickL_upper)
    xLT, yLT, ptsLT = findCenter(image, config.tipL_lower, config.tipL_upper)

    vR= [(xRT-xRS), (yRT-yRS)]
    vL= [(xLT-xLS), (yLT-yLS)] 
    
    return math.degrees(angle(vR, vL))

def dist(x1,y1,x2,y2, scale = 1):
    return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))* scale
''' convert x,y position to coordinates- mainly for overhead camera video processing '''
def mat2coord(shape, x, y):
    xp = x -int(shape[1]/2)
    yp = int(shape[0]/2) - y
    return xp, yp

''' Return numpy arrays of height, and possibly left or right for each hit? '''
def sideProcess(vidPath, fs = 120):
    cap = cv2.VideoCapture(vidPath)
    heights = np.empty((3,0))
    fc = 0
    timestep = (1/fs)*1000
    while cap.isOpened():
        ret, image = cap.read()
        if ret is False:
            cap.release()
            break
        hl, hr= getHeights(image)

        heights = np.hstack((heights, np.array([[timestep*fc],[hl],[hr]])))
        fc = fc+1
        if '-s' in sys.argv:
            cv2.imshow('SideView', image)
        cv2.waitKey(1)
    if '-s' in sys.argv:
        cv2.destroyWindow('SideView')

    return heights

''' return numpy arrays of stick angle and possibly finer positions for tips '''
def ohProcess(vidPath, fs = 120):
    cap = cv2.VideoCapture(vidPath)
    angles = np.empty((2,0))
    fc = 0 # frame count
    timestep = (1/fs)*1000 #time difference per frame, based on fps
    while cap.isOpened():
        ret, image = cap.read()
        if ret is False:
            cap.release()
            break
        # ang= stickAngle(image)
        ang = vecAngle(image)
        angles= np.hstack((angles, np.array([[timestep*fc], [ang]])))
        fc = fc+1
        if '-s' in sys.argv:
            cv2.imshow('OHView', cv2.resize(image, (0,0), fx = 0.5, fy = 0.5))
        if '-d' in sys.argv:
            print ang
        cv2.waitKey(1)

    if '-s' in sys.argv:
        cv2.destroyWindow('OHView')
    return angles