''' GUI Controller and Wrapper for Drum Trainer
    Hilary Mogul - hilary.mogul@gmail.com
'''

import numpy as np
import os
import sys
import cv2
import Tkinter
import matplotlib.pyplot as plt
import tkMessageBox
import tkFileDialog
sys.path.append("libraries")
# self made libraries
import readHits
import imageFunctions as img
import performance_analysis as perf
import config as cfg

root= Tkinter.Tk()
root.title("Drum Trainer")
path = Tkinter.StringVar()
root.configure(background = 'black')
def quit():
	root.quit()

def credits():
	tkMessageBox.showinfo("Credits", "Team ColDRUMbia 5ever")
#initial window
def viewInit():
	frameI = Tkinter.Frame(root)
	frameI.grid()
	label = Tkinter.Label(frameI, text = "DRUM TRAINER PROGRAM", relief = Tkinter.RAISED)
	label.grid(row = 0, column = 1)
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
	clearOut(root)
	frame0 = Tkinter.Frame(root)
	frame0.grid()
	
	nameLabel = Tkinter.Label(frame0, text = "Name of Example/Folder")
	nameLabel.grid(row = 0,column = 0)

	nameEntry = Tkinter.Entry(frame0, text = "Example")
	nameEntry.grid(row = 1,column = 0)
	

	global path
	pathLabel = Tkinter.Label(frame0, text = "Path for Example to be saved")
	pathLabel.grid(row = 2, column = 0)
	path.set(cfg.userPath)
	pathShow = Tkinter.Label(frame0, textvariable = path, relief = Tkinter.SUNKEN)
	pathShow.grid(row = 3, column = 0)

	pathButton = Tkinter.Button(frame0, text = "...", command = pathOpen)
	pathButton.grid(row = 3, column = 1)

def pathOpen():
	path.set(tkFileDialog.askdirectory(parent = root))
	cfg.userPath = path.get()
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
