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
import shutil

sys.path.append("libraries")
# self made libraries
import readHits
import imageFunctions as img
import performance_analysis as perf
import config as cfg

root= Tkinter.Tk()
root.title("Drum Trainer")
root.columnconfigure(0, weight=1)
userpath = Tkinter.StringVar()
gtpath = Tkinter.StringVar()
tempo = Tkinter.IntVar()
duration = Tkinter.IntVar()
nameFolder = Tkinter.StringVar()
def quit():
	root.quit()
def reset():
	cfg.resetAll()
	userpath.set('')
	gtpath.set('')
	tempo.set(40)
	duration.set(0)
	nameFolder.set('')
def credits():
	tkMessageBox.showinfo("Credits", "Team ColDRUMbia 5ever")
#initial window
def viewInit():
	clearOut(root)
	cfg.resetAll()
	reset()
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
	tempoEntry = Tkinter.Spinbox(frame0, from_ = 40, to = 240, textvariable = tempo, command  = setTempDur).grid(row = 5, column = 0)
	
	durationLabel = Tkinter.Label(frame0, text = "Duration (seconds)").grid(row = 6, column = 0)
	durationEntry = Tkinter.Spinbox(frame0, from_ = 1, to = 300, textvariable = duration, command = setTempDur).grid(row = 7, column = 0)

	# arduino selection boxes
	serialList = readHits.serial_ports()
	unoLabel = Tkinter.Label(frame0, text = "Address of UNO (Camera Controller)").grid(row = 8, column = 0)
	unoBox = Tkinter.Listbox(frame0, selectmode = Tkinter.SINGLE)
	for address in serialList:
		unoBox.insert(Tkinter.END, address)
	megaLabel = Tkinter.Label(frame0, text = "Address of Mega (Sensor Reader)").grid(row = 9, column = 0)
	megaBox = Tkinter.Listbox(frame0, selectmode = Tkinter.SINGLE)
	for address in serialList:
		megaBox.insert(Tkinter.END, address)
	unoBox.grid(row = 8, column = 1)
	megaBox.grid(row = 9, column = 1)
	def unoSelect(evt):
		cfg.unoPath = unoBox.get(unoBox.curselection())
	def megaSelect(evt):
		cfg.megaPath = megaBox.get(megaBox.curselection())
	unoBox.bind('<<ListboxSelect>>', unoSelect)
	megaBox.bind('<<ListboxSelect>>', megaSelect)

	homeButton = Tkinter.Button(frame0, text = "Back", command = viewInit).grid(row = 0, column = 5)
	# TODO: reset fields function outside of this loop?
	resetButton = Tkinter.Button(frame0, text = "Reset", command = reset).grid(row = 1, column = 5)
	
	startButton = Tkinter.Button(frame0, text = "START", command = option0_start, bg = 'GREEN').grid(row = 2, column = 5)
	padWidgets(frame0)
	return
def option0_start():
	#TODO: function to pick up/set all appropriate values
	# check if os join of path and name folder exists, and if it does, return a message box
	if os.path.isdir(os.path.join(cfg.userPath, nameFolder.get())):
		tkMessageBox.showinfo("ERROR", "Folder already exists! Pick another")
		return
	# check for empty strings
	elif len(nameFolder.get()) ==0  or duration.get() is None or len(userpath.get()) == 0 or cfg.unoPath is '' or cfg.megaPath is '' or cfg.megaPath is cfg.unoPath:
		tkMessageBox.showinfo("ERROR", "Missing data, please fill in everything")
		return
	cfg.userFolder = nameFolder.get()
	os.mkdir(os.path.join(cfg.userPath, cfg.userFolder))
	clearOut(root)
	frame0A = Tkinter.Frame(root).grid()
	# maybe make a thing that flashes based on tempo in recording adjustment thread? if tempo is set, that is
	nowRecording = Tkinter.Label(frame0A, text = "NOW RECORDING", bg = 'GREEN').grid()

	#time.sleep(0.1)
	mega = readHits.megaComm(1, "MegaComm", spoof = True)
	uno = readHits.unoComm(2, "UnoComm", spoof = True)
	uno.start()
	time.sleep(.0001)
	mega.start()
	# debug printing TODO: dummy out, and set spoof to False
	print "RECORDING NOW AT"
	print time.localtime()
	uno.join()
	mega.join()
	print "FINISHING RECORDING"
	print time.localtime()
	cameraInstructions(0)
	return
'''File prompts for video files to be processed
   0 = option 0- initial just copy and process to be used as ground truth/funsies
   1- option 1 - review existing attempt.  prob wont be used
   2- option 2- record new attempt.  copy, process, compare as ground truth
'''
def cameraInstructions(choice = 0):
	ohPath = Tkinter.StringVar()
	sidePath = Tkinter.StringVar()
	frontPath = Tkinter.StringVar()
	def setOH():
		ohPath.set(tkFileDialog.askopenfilename(defaultextension = '.avi'))
		return
	def setSide():
		sidePath.set(tkFileDialog.askopenfilename(defaultextension = '.avi'))
		return
	def setFront():
		frontPath.set(tkFileDialog.askopenfilename(defaultextension = '.avi'))
		return
	tkMessageBox.showinfo("Instructions for Camera Access", "Plug in camera USB hub and select Overhead, Side, and Front video files respectively")
	clearOut(root)
	camFrame = Tkinter.Frame(root).grid()
	# list of labels and textentries with buttons next to them for files
	ohLabel = Tkinter.Label(camFrame, text ="Overhead View File").grid(row = 1, column = 0)
	ohEntry = Tkinter.Label(camFrame, textvariable = ohPath, relief = Tkinter.SUNKEN).grid(row =2, column = 0)
	ohButton = Tkinter.Button(camFrame, text = "...", command = setOH).grid(row = 2, column = 1)	
	
	sideLabel = Tkinter.Label(camFrame, text ="Side View File").grid(row = 3, column = 0)
	sideEntry = Tkinter.Label(camFrame, textvariable = sidePath, relief = Tkinter.SUNKEN).grid(row =4, column = 0)
	sideButton = Tkinter.Button(camFrame, text = "...", command = setSide).grid(row = 4, column = 1)	

	frontLabel = Tkinter.Label(camFrame, text ="Front View File").grid(row = 5, column = 0)
	frontEntry = Tkinter.Label(camFrame, textvariable = frontPath, relief = Tkinter.SUNKEN).grid(row =6, column = 0)
	frontButton = Tkinter.Button(camFrame, text = "...", command = setFront).grid(row = 6, column = 1)	
	
	def continueProcess0():
		# TODO: check option choice, and based on that decide to process alone or correlate with ground truth
		if os.path.isfile(sidePath.get()) and os.path.isfile(ohpath.get()):
			cfg.userHeights = img.sideProcess(sidePath.get())
			cfg.userAngles = img.ohProcess(ohPath.get())
			shutil.copy2(sidePath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi'))
			shutil.copy2(ohPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi'))
			shutil.copy2(frontPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'frontView.avi'))
			# TODO: run image processing
		else:
			tkMessageBox.showinfo("ERROR", "Invalid files, try again")


		pass
	if choice ==0:
		nextButton = Tkinter.Button(camFrame, text = "Continue", command = continueProcess0).grid(row =3, column =5)
	else:
		print "NOT THERE YET"
	
''' Set path of user entry, bound to work bc of folder selection
0 = path of user folder
1 = path of GT folder
TODO: check in gt folder that there are correct files- and load the tempo
and duration for each
'''
def pathOpen(option = 0):
	if option is 0:
		userpath.set(tkFileDialog.askdirectory(parent = root))
		cfg.userPath = userpath.get()
	elif option is 1:
		gtpath.set(tkFileDialog.askdirectory(parent = root))
		if os.path.isfile(os.path.join(gtpath.get(), 'data.mat')):
			cfg.gtPath = gtpath.get()
			cfg.loadGT()
			tempo.set(cfg.tempo)
			duration.set(cfg.duration)
		else:
			tkMessageBox.showinfo('ERROR', 'Missing data file.  Please choose a different folder.')

''' things for reviewing an existing attempt.  should be able to just loadmat this
	then process the output files
 '''
def option1():
	#TODO: label/entry/button for path for gt and user paths
	# then run same functions as option2 after recording?
	pass

''' recording a new attempt.  follows procession of first, with side note of selecting GT folder '''
def option2():
	clearOut(root)
	frame2 = Tkinter.Frame(root)
	frame2.grid()


	nameLabel = Tkinter.Label(frame2, text = "Name of Attempt")
	nameLabel.grid(row = 0,column = 0)

	nameEntry = Tkinter.Entry(frame2, textvariable = nameFolder)
	nameEntry.grid(row = 1,column = 0)


	pathLabel = Tkinter.Label(frame2, text = "Path for Attempt to be saved")
	pathLabel.grid(row = 2, column = 0)
	userpath.set(cfg.userPath)
	pathShow = Tkinter.Label(frame2, textvariable = userpath, relief = Tkinter.SUNKEN)
	pathShow.grid(row = 3, column = 0)

	pathButton = Tkinter.Button(frame2, text = "...", command = lambda: pathOpen(option =0))
	pathButton.grid(row = 3, column = 1)

	gtLabel = Tkinter.Label(frame2, text ="Path of Example to Follow").grid(row=4, column = 0)
	gtpathShow = Tkinter.Label(frame2, textvariable = gtpath, relief = Tkinter.SUNKEN).grid(row = 5, column = 0)
	gtButton = Tkinter.Button(frame2, text = "...", command = lambda: pathOpen(option =1)).grid(row=5, column = 1)

	
	# arduino selection boxes
	xScroll = Tkinter.Scrollbar(frame2, orient = Tkinter.HORIZONTAL).grid(row)

	serialList = readHits.serial_ports()
	unoLabel = Tkinter.Label(frame2, text = "Address of UNO (Camera Controller)").grid(row = 8, column = 0)
	unoBox = Tkinter.Listbox(frame2, selectmode = Tkinter.SINGLE)
	for address in serialList:
		unoBox.insert(Tkinter.END, address)
	megaLabel = Tkinter.Label(frame2, text = "Address of Mega (Sensor Reader)").grid(row = 9, column = 0)
	megaBox = Tkinter.Listbox(frame2, selectmode = Tkinter.SINGLE)
	for address in serialList:
		megaBox.insert(Tkinter.END, address)
	unoBox.grid(row = 8, column = 1)
	megaBox.grid(row = 9, column = 1)
	def unoSelect(evt):
		cfg.unoPath = unoBox.get(unoBox.curselection())
	def megaSelect(evt):
		cfg.megaPath = megaBox.get(megaBox.curselection())
	unoBox.bind('<<ListboxSelect>>', unoSelect)
	megaBox.bind('<<ListboxSelect>>', megaSelect)

	homeButton = Tkinter.Button(frame2, text = "Back", command = viewInit).grid(row = 0, column = 5)
	# TODO: reset fields function outside of this loop?
	resetButton = Tkinter.Button(frame2, text = "Reset", command = reset).grid(row = 1, column = 5)
	
	startButton = Tkinter.Button(frame2, text = "START", command = option2_start, bg = 'GREEN').grid(row = 2, column = 5)
	


	padWidgets(frame2)

def option2_start():
	pass


''' if i get fluid synth going, make an instrument version '''
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
