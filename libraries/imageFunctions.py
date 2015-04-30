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
def getHeightRaw(image, hsv, scale =1):
    x, y, pts = findCenter(image, hsv[0],hsv[1])
    if isNan(x) or pts < config.ptsThresh:
        return -1
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
def getAngle(image, hsv1, hsv2, right = False):
    x1, y1, pts1 = findCenter(image, hsv1[0], hsv1[1])
    y1 = image.shape[0]- y1
    x2, y2, pts2 = findCenter(image, hsv2[0], hsv2[1])
    # x2, y2 = mat2coord(image.shape, x1,y1)
    y2 = image.shape[0]- y2

    # print "{0}, {1}".format(x2, y2)
    if not isNan(x1) and not isNan(x2) and min(pts1, pts2)> config.ptsThresh:

        y1 = image.shape[0]-y1
        y2 = image.shape[0]-y2

        if right:
            if x2 < x1:
                return math.degrees(math.atan((x1-x2)/math.fabs(y2-y1)))
            # stick not pointed towards center in this case
            else:
                return None
        # for left stick
        else:
            if x2 > x1:
                return math.degrees(math.atan((x2-x1)/math.fabs(y2-y1)))
            else:
                return None
        # slope = (y1-y2)/(x1-x2)
        # # print "DEBUG MODE SLOPE IS {}".format(slope)
        # # print  math.degrees(math.atan(slope))
        # return math.degrees(math.atan(slope))
    else:
        return None
''' uses config hsv bounds to find angle between 2 sticks '''
def stickAngle(image):
    angleR = getAngle(image, np.vstack((config.stickR_lower, config.stickR_upper)), np.vstack((config.tipR_lower, config.tipR_upper)), right = True)
    angleL = getAngle(image, np.vstack((config.stickL_lower, config.stickL_upper)), np.vstack((config.tipL_lower, config.tipL_upper)))
    print angleR
    print angleL
    if angleR is None or angleL is None:
        return None
    else:
        return angleR+angleL

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
        hL= getHeightRaw(image, np.vstack((config.tipL_lower, config.tipL_upper)))
        hR= getHeightRaw(image, np.vstack((config.tipR_lower, config.tipR_upper)))

        heights = np.hstack((heights, np.array([[timestep*fc],[hL],[hR]])))
        fc = fc+1
        if '-d' in sys.argv:
            cv2.imshow('SideView', image)
        cv2.waitKey(1)
    if '-d' in sys.argv:
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
        ang= stickAngle(image)
        angles= np.hstack((angles, np.array([[timestep*fc], [ang]])))
        fc = fc+1
        cv2.waitKey(1)
    return angles

# ''' Uses default user webcam to show images, and possibly write to file as well'''
# def webCamRun(saving = False, showing = False):
#     cap = cv2.VideoCapture(0)
#     _, frame = cap.read()
#     print "At start of webCamRun"
#     if saving:
#         print "initializing VideoWriter"
#         vid = cv2.VideoWriter(os.path.join(config.userPath, config.userFolder, 'CamView.avi'), fourcc = cv2.CV_FOURCC('H','2','6','4'), fps = 30, frame_size = frame.shape)
#         suc = vid.open()
#     while(config.recording or config.playing):
#         print "in collection loop"
#         _, frame = cap.read()
#         if showing:
#             # cv2.imshow('Webcam image', frame)
#             pass
#         if saving:
#             vid.write(frame)
    



# ''' Thread for showing webcam footage, and possibly saving it to file '''
# class webCam(threading.Thread):
#     def __init__(self, threadID, name, saving, showing):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.saving = saving
#         self.showing = showing
#         print "Im initialized!"
#     def run(self):
#         print "IN start"
#         webCamRun(self.saving, self.showing)


