
import cv2
import numpy as np
import os
import sys

filepath = "/Users/hilarymogul/Downloads/Edwin_test_different_angle.AVI"
print os.path.isfile(filepath)
cap = cv2.VideoCapture(filepath)
# cap.set(cv2.CV_CAP_PROP_FOURCC, cv2.CV_FOURCC('H','2','6','4'))
# print cap.get(cv2.CV_CAP_PROP_FOURCC)
framec = 0
dr = cv2.namedWindow('drum')
if len(sys.argv) > 1:
	delay = int(sys.argv[1])
else:
	delay = 10
while(cap.isOpened()):
	# retval= cap.grab()
	# if retval is False:
	# 	print "Closed at retval is false"
	# 	cap.release()
	# 	break
	ret , image = cap.read()
	if ret is False:
		cap.release()
		break
	cv2.imshow('drum', image)
	framec = framec+1
	k = cv2.waitKey(delay) & 0xFF
	if k ==27:
		break
cv2.destroyWindow('drum')
print "Frame count is {0}".format(framec)
