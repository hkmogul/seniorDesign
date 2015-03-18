''' Main program to run for senior design project '''

import Tkinter
import numpy as np
import cv2
import scipy.io
import matplotlib.pyplot as plt
import os
import sys

sys.path.append("libraries")
# user defined libraries
import imageFunctions as img
import config as cfg
import performance_analysis as perf
import readHits

root = Tkinter.Tk()
f1 = True
def frame2():
	nextFrame = Tkinter.Frame(root)
	nextFrame.pack()
	Button2 = Tkinter.Button(nextFrame, text = "Press me to go to frame1", command = switchBack)
	Button2.pack(side = Tkinter.RIGHT)

def switchBack():
	global f1
	clearOut(root)
	if f1:
		f1 = False
		frame2()
	else:
		f1 = True
		frame1()

def clearOut(parent):
	for widget in parent.winfo_children():
		widget.destroy()

def frame1():
	frame = Tkinter.Frame(root)
	frame.pack()
	Button1 = Tkinter.Button(frame, text = "Press me to go to frame2", command = switchBack)
	Button1.pack(side = Tkinter.LEFT)


frame1()
root.mainloop()











root.mainloop()
