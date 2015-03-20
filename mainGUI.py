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
import threading
import time

sys.path.append("libraries")
# self made libraries
import readHits
import imageFunctions as img
import performance_analysis as perf
import config as cfg

root= Tkinter.Tk()
root.title("Drum Trainer")
userpath = Tkinter.StringVar()
gtpath = Tkinter.StringVar()
tempo = Tkinter.IntVar()
duration = Tkinter.IntVar()
nameFolder = Tkinter.StringVar()
ohVid = Tkinter.StringVar()
sideVid = Tkinter.StringVar()
frontVid = Tkinter.StringVar()
def quit():
	root.quit()
def reset():
	cfg.resetAll()
def credits():
	tkMessageBox.showinfo("Credits", "Team ColDRUMbia 5ever")
#initial window
def viewInit():
	clearOut(root)
	cfg.resetAll()
	frameI = Tkinter.Frame(root)
	frameI.pack()
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

	padWidgets(frameI)
def option0():
	clearOut(root)
	frame0 = Tkinter.Frame(root)
	frame0.grid()

	nameLabel = Tkinter.Label(frame0, text = "Name of Example/Folder")
	nameLabel.grid(row = 0,column = 0)

	nameEntry = Tkinter.Entry(frame0, textvariable = nameFolder)
	nameEntry.grid(row = 1,column = 0)


	global userpath
	pathLabel = Tkinter.Label(frame0, text = "Path for Example to be saved")
	pathLabel.grid(row = 2, column = 0)
	userpath.set(cfg.userPath)
	pathShow = Tkinter.Label(frame0, textvariable = userpath, relief = Tkinter.SUNKEN)
	pathShow.grid(row = 3, column = 0)

	pathButton = Tkinter.Button(frame0, text = "...", command = pathOpen)
	pathButton.grid(row = 3, column = 1)

	tempoLabel = Tkinter.Label(frame0, text = "TEMPO (bpm)").grid(row = 4, column = 0)
	#TODO: validation function for numbers only
	tempoEntry = Tkinter.Spinbox(frame0, from_ = 40, to = 240, textvariable = tempo, command  = setTempDur).grid(row = 5, column = 0)
	
	durationLabel = Tkinter.Label(frame0, text = "Duration (seconds)").grid(row = 6, column = 0)
	durationEntry = Tkinter.Spinbox(frame0, from_ = 1, to = 300, textvariable = duration, command = setTempDur).grid(row = 7, column = 0)

	homeButton = Tkinter.Button(frame0, text = "Back", command = viewInit).grid(row = 0, column = 5)
	# TODO: reset fields function outside of this loop?
	resetButton = Tkinter.Button(frame0, text = "Reset", command = reset).grid(row = 1, column = 5)
	
	startButton = Tkinter.Button(frame0, text = "START", command = option0_start, bg = 'GREEN').grid(row = 2, column = 5)
	padWidgets(frame0)
	return
def option0_start():
	#TODO: function to pick up/set all appropriate values
	# check if os join of path and name folder exists, and if it does, return a message box
	if os.path.isdir(os.path.join(cfg.userPath, userFolder.get())):
		tkMessageBox.showinfo("ERROR", "Folder already exists! Pick another")
		return
	cfg.userFolder = userFolder.get()
	os.mkdir(os.path.join(cfg.userpath, cfg.userFolder))
	clearOut(root)
	frame0A = Tkinter.Frame(root).grid()
	# maybe make a thing that flashes based on tempo in recording adjustment thread? if tempo is set, that is
	nowRecording = Tkinter.Label(root, text = "NOW RECORDING", bg = 'GREEN').grid()
	mega = readHits.megaComm(1, "MegaComm", spoof = True)
	uno = readHits.unoComm(2, "UnoComm", spoof = True)
	uno.start()
	time.sleep(.0001)
	mega.start()
	uno.join()
	mega.join()
	cameraInstructions0()
	return

def cameraInstructions0():
	tkMessageBox.showinfo("Instructions for Camera Access", "Plug in camera USB hub and select Overhead, Side, and Front video files respectively")
	clearOut(root)
	camFrame = Tkinter.Frame(root).pack()


''' Set path of user entry, bound to work bc of folder selection
0 = path of user folder
1 = path of GT folder
'''
def pathOpen(option = 0):
	if option is 0:
		userpath.set(tkFileDialog.askdirectory(parent = root))
		cfg.userPath = userpath.get()
	elif option is 1:
		gtpath.set(tkFileDialog.askdirectory(parent = root))
		cfg.gtPath = gtpath.get()

''' set path of file entry, based on different options
0 = path of overhead camera
1 = path of side camera
2 = path of front camera

'''
def fileChoose(option = 0):
	if option is 0:
		ohVid.set(tkFileDialog.askopenfilename(parent = root, defaultextension = '.avi'))
	elif option is 1:
		sideVid.set(tkFileDialog.askopenfilename(parent = root, defaultextension = '.avi'))
	elif option is 2:
		frontVid.set(tkFileDialog.askopenfilename(parent = root, defaultextension = '.avi'))

def option1():

	pass
def option2():
	pass
def option3():
	pass
def FUN():
	print "AWWW YEEAAAHHHH"
	pass
''' Empties all widgets out of a parent '''
def clearOut(parent):
	for widget in parent.winfo_children():
		widget.destroy()

''' Gives all widgets in a parent some space '''
def padWidgets(parent):
	for widget in parent.winfo_children():
		widget.grid(padx = 5, pady = 2)
def setTempDur():
	cfg.tempo = tempo.get()
	cfg.duration = duration.get()
viewInit()

root.mainloop()
