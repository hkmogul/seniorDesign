''' Utilities for processing images (such as height, angle, etc) '''

import numpy as np
import cv2
import math
import config

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
def getHeightRaw(image, hsv, scale =1):
    x, y, pts = findCenter(image, hsv[0],hsv[1])
    if isNan(x) or pts < config.ptsThresh:
        return None
    else:
        return (image.shape[0]-y)*scale

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
''' get angle of single stick.  hsv1 and hsv2 correlate to stick hsv thresholds'''
def getAngle(image, hsv1, hsv2):
    x1, y1, pts1 = findCenter(image, hsv1[0], hsv1[1])
    x1, y1 = mat2coord(image.shape, x1,y1)
    x2, y2, pts2 = findCenter(image, hsv2[0], hsv2[1])
    x2, y2 = mat2coord(image.shape, x1,y1)

    if not isNan(x1) and not isNan(x2) and min(pts1, pts2)> config.ptsThresh:

        y1 = image.shape[0]-y1
        y2 = image.shape[0]-y2
        slope = (y1-y2)/(x1,x2)
        return math.degrees(math.atan(slope))
    else:
        return None
''' uses config hsv bounds to find angle between 2 sticks '''
def stickAngle(image):
    angleR = getAngle(image, np.vstack((config.stickR_lower, config.stickR_upper)), np.vstack((config.tipR_lower, config.tipR_upper)))
    angleL = getAngle(image, np.vstack((config.stickL_lower, config.stickL_upper)), np.vstack((config.tipL_lower, config.tipL_upper)))
    if angleR is None or angleL is None:
        return None
    else:
        return 180-angleR-angleL

def dist(x1,y1,x2,y2, scale = 1):
    return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))* scale
''' convert x,y position to coordinates- mainly for overhead camera video processing '''
def mat2coord(shape, x, y):
    xp = x -int(shape[1]/2)
    yp = int(shape[0]/2) - y
    return xp, yp
