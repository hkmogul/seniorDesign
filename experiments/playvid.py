
import cv2
import numpy as np
import os

filepath = "/Users/hilarymogul/Downloads/Edwin_test_different_angle.AVI"
print os.path.isfile(filepath)
cap = cv2.VideoCapture(filepath)
# cap.set(cv2.CV_CAP_PROP_FOURCC, cv2.CV_FOURCC('H','2','6','4'))
print cv2.get(cv2.CV_CAP_PROP_FPS)
print cap.isOpened()
while(cap.isOpened()):
	# retval= cap.grab()
	# if retval is False:
	# 	print "Closed at retval is false"
	# 	cap.release()
	# 	break
	ret , image = cap.read()
	print type(image)
	if ret is False:
		print "Closed at ret is false"
		cap.release()
		break
	cv2.imshow('drum', image)
	cv2.waitkey(100)
cv2.destroyAllWindows()
