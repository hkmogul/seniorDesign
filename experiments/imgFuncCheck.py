''' Copied code for tracking colored objects.  Will start with the straw of my cup '''

import cv2
import numpy as np
import imageFunctions as img

def findPosition(mask):
    points = np.where(mask)
    return np.median(points[0]), np.median(points[1]), points[0].shape[0]

def isNaN(num):
    return num != num

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of orange color in HSV
    lower_orange = np.array([7,175,175])
    upper_orange = np.array([15,255,255])

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    #find contours from bitmask
    contours,hierarchy = cv2.findContours(mask, 1,2)

    # cv2.resizeWindow('frame', 500,500)
    # cv2.imshow('mask',mask)
    # cv2.resizeWindow('mask', 500,500)
    y, x, pts = findPosition(mask)
    if isNaN(x) or pts < 500:
        print "BALL NOT FOUND"
        print frame.shape
    else:
        # frame[(max(y-10,0)):min(y+10, 1080)][x][0] = 0
        frame[y][x][0] =0
        frame[y][x][1]= 255
        frame[y][x][2] = 0
        res[y][x][0] = 0
        res[y][x][1]= 255
        res[y][x][2] = 0
        # if len(contours) is not 0:
        #     cnt = contours[0]
        #     print cnt
        #     M = cv2.moments(cnt)
        #     # cx = int(M['m10']/M['m00'])
        #     # cy = int(M['m01']/M['m00'])
        print "X: {0}, Y: {1}, #pts = {2}".format(x, y, pts)
        x2,y2,ptx2 = img.findCenter(frame, lower_orange, upper_orange)

        print "X2: {0}, Y2: {1}, second pts = {2}".format(x2, y2, pts)
        # print "CX: {0}, CY: {1}".format(cx, cy)

    cv2.imshow('res',res)
    # cv2.resizeWindow('res', 500,500)

    # cv2.imshow('frame',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print " you pressed 'a'!"

cv2.destroyAllWindows()
