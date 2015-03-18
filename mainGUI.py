''' GUI Controller and Wrapper for Drum Trainer
    Hilary Mogul - hilary.mogul@gmail.com
'''

import numpy as np
import os
import sys
import cv2
import Tkinter
import matplotlib.pyplot as plt
#import tkFont
import tkMessageBox

sys.path.append("libraries")
# self made libraries
import readHits
import imageFunctions as img
import performance_analysis as perf
import config as cfg

# helv16 = tkFont.Font(family = "Helvetica",size =  16)
root= Tkinter.Tk()
# initial opening window
def quit():
	root.quit()

def credits():
	tkMessageBox.showinfo("Credits", "Team ColDRUMbia 5ever")

def viewInit():
	frameI = Tkinter.Frame(root)
	frameI.pack()
	label = Tkinter.Label(frameI, text = "DRUM TRAINER PROGRAM", relief = Tkinter.RAISED)
	label.grid(row = 0, column = 1)
#	global helv16
	button0 = Tkinter.Button(frameI, text = "Record new Example", command = option0)
	button0.grid(row = 1, column = 1)

	button1 = Tkinter.Button(frameI, text = "Review Existing Attempt", command = option1)
	button1.grid(row = 3, column=1)

	button2 = Tkinter.Button(frameI, text = "Record new Attempt", command = option2)
	button2.grid(row = 5, column = 1)

	button3 = Tkinter.Button(frameI, text = "FUN MODE", command = FUN)
	button3.grid(row = 7, column = 1)

	quitButton = Tkinter.Button(frameI, text = "QUIT", command = quit)
	quitButton.grid(row = 9, column =2)
	
	creditB = Tkinter.Button(frameI, text = "CREDITS", command = credits)
	creditB.grid(row = 9, column = 0)

def option0():
	pass
def option1():
	pass
def option2():
	pass
def option3():
	pass
def FUN():
	print "AWWW YEEAAAHHHH"
	pass








def clearOut(parent):
	for widget in parent.winfo_children():
		widget.destroy()

viewInit()

root.mainloop()
