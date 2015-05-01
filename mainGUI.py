''' GUI Controller and Wrapper for Drum Trainer
    Hilary Mogul - hilary.mogul@gmail.com
'''

import numpy as np
import os
import sys
import cv2
import Tkinter
# import ImageTk
import matplotlib.pyplot as plt
import tkMessageBox
import tkFileDialog
import threading
import time
import shutil

from datetime import datetime

sys.path.append("libraries")
# self made libraries
import readHits
import imageFunctions as img
import performance_analysis as perf
import config as cfg

debug = False
if '-d' in sys.argv:
	debug = True


root= Tkinter.Tk()
root.title("Drum Trainer")
root.columnconfigure(0, weight=1)
userpath = Tkinter.StringVar()
gtpath = Tkinter.StringVar()
tempo = Tkinter.IntVar()
duration = Tkinter.IntVar()
nameFolder = Tkinter.StringVar()
recVar = Tkinter.IntVar()
showVar = Tkinter.IntVar()
skipGrade = Tkinter.IntVar()
sf2 = Tkinter.StringVar()
octave = Tkinter.IntVar()
def quit():
	root.quit()
def reset():
	cfg.resetAll()
	userpath.set('')
	gtpath.set('')
	tempo.set(40)
	duration.set(0)
	nameFolder.set('')
	recVar.set(0)
	showVar.set(0)
	skipGrade.set(0)
	octave.set(4)
	readHits.octave = 4

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

	nameEntry = Tkinter.Entry(frame0, textvariable = nameFolder, width = 75)
	nameEntry.grid(row = 1,column = 0)


	# global userpath
	pathLabel = Tkinter.Label(frame0, text = "Path for Example to be saved")
	pathLabel.grid(row = 2, column = 0)
	userpath.set(cfg.userPath)
	pathShow = Tkinter.Label(frame0, textvariable = userpath, relief = Tkinter.SUNKEN, width = 75)
	pathShow.grid(row = 3, column = 0)

	pathButton = Tkinter.Button(frame0, text = "...", command = pathOpen)
	pathButton.grid(row = 3, column = 1)

	tempoLabel = Tkinter.Label(frame0, text = "TEMPO (bpm)").grid(row = 4, column = 0)
	tempoEntry = Tkinter.Spinbox(frame0, from_ = 40, to = 240, textvariable = tempo, command  = setTempDur).grid(row = 5, column = 0)
	
	durationLabel = Tkinter.Label(frame0, text = "Duration (seconds)").grid(row = 6, column = 0)
	durationEntry = Tkinter.Spinbox(frame0, from_ = 1, to = 300, textvariable = duration, command = setTempDur).grid(row = 7, column = 0)
	



	# arduino selection boxes
	serialList = readHits.serial_ports()
	tempty = []
	# if serialList == tempty and not debug:
	# 	tkMessageBox.showinfo('ERROR', 'No serial ports found!')
	# 	clearOut(root)
	# 	viewInit()
	unoLabel = Tkinter.Label(frame0, text = "Address of UNO (Camera Controller)")
	unoLabel.grid(row = 8, column = 0)
	unoBox = Tkinter.Listbox(frame0, selectmode = Tkinter.SINGLE, width = 75)
	for address in serialList:
		unoBox.insert(Tkinter.END, address)
	megaLabel = Tkinter.Label(frame0, text = "Address of Mega (Sensor Reader)").grid(row = 9, column = 0)
	megaBox = Tkinter.Listbox(frame0, selectmode = Tkinter.SINGLE, width = 75)
	for address in serialList:
		megaBox.insert(Tkinter.END, address)
	unoBox.grid(row = 8, column = 3)
	megaBox.grid(row = 10, column = 3)
	megaScroll = Tkinter.Scrollbar(frame0, orient = Tkinter.HORIZONTAL)
	megaScroll.grid(row = 11, column =3, sticky = Tkinter.E+ Tkinter.W)
	unoScroll = Tkinter.Scrollbar(frame0, orient = Tkinter.HORIZONTAL)
	unoScroll.grid(row = 9, column = 3, sticky = Tkinter.E+ Tkinter.W)
	megaBox.config(xscrollcommand = megaScroll.set)
	megaScroll.config(command = megaBox.xview)
	unoBox.config(xscrollcommand = unoScroll.set)
	unoScroll.config(command = unoBox.xview)
	def unoSelect(evt):
		cfg.unoPath = unoBox.get(unoBox.curselection())
	def megaSelect(evt):
		cfg.megaPath = megaBox.get(megaBox.curselection())
	unoBox.bind('<<ListboxSelect>>', unoSelect)
	megaBox.bind('<<ListboxSelect>>', megaSelect)

	# checkboxes for if webcam is being used in this session
	recCheck = Tkinter.Checkbutton(frame0, text = "Record With Webcam", variable = recVar)
	showCheck = Tkinter.Checkbutton(frame0, text = "Show Webcam View While Playing", variable = showVar)
	recCheck.grid(row = 0, column = 3)
	showCheck.grid(row = 1, column = 3)

	homeButton = Tkinter.Button(frame0, text = "Back", command = viewInit).grid(row = 0, column = 5)
	resetButton = Tkinter.Button(frame0, text = "Reset", command = reset).grid(row = 1, column = 5)
	startButton = Tkinter.Button(frame0, text = "START", command = option0_preStart, bg = 'GREEN').grid(row = 2, column = 5)

	#give everything some space
	padWidgets(frame0)
	return
''' lets see if this fixes GUI issue '''
def option0_preStart():

	# check if os join of path and name folder exists, and if it does, return a message box
	if os.path.isdir(os.path.join(cfg.userPath, nameFolder.get())):

		tkMessageBox.showinfo("ERROR", "Folder already exists! Pick another")
		return
	# check for empty strings
	elif len(nameFolder.get()) ==0  or duration.get() is None or len(userpath.get()) == 0 or cfg.unoPath is '' or cfg.megaPath is '' or cfg.megaPath is cfg.unoPath:
		tkMessageBox.showinfo("ERROR", "Missing data, please fill in everything")
		return
	else:
		clearOut(root)
		frameC = Tkinter.Frame(root)
		frameC.grid()
		countLabel = Tkinter.Label(frameC, text = 3, bg = 'YELLOW', font = ('Helvetica', 72))
		countLabel.grid()
		# option0_start()
		countdown(3, countLabel)

# count = 3
def countdown(count, label):

	if count <0:
		option0_start()
	else:
		if count is 0:
			label.configure(bg = 'GREEN')
		label.configure(text = count)
		count = count-1
		root.after(1000, countdown, count, label)
		# countdown(count, label)
def option0_start():
	clearOut(root)
	frame0A = Tkinter.Frame(root)
	frame0A.grid()
	nowRecording = Tkinter.Label(frame0A, text = "FINISHED RECORDING", bg = 'YELLOW', font = ('Helvetica', 72))
	nowRecording.grid()

	cfg.userFolder = nameFolder.get()
	os.mkdir(os.path.join(cfg.userPath, cfg.userFolder))

	if debug:
		mega = readHits.megaComm(1, "MegaComm", spoof = True)
		uno = readHits.unoComm(2, "UnoComm", spoof = True)
	else:
		mega = readHits.megaComm(1, "MegaComm", spoof = False)
		uno = readHits.unoComm(2, "UnoComm", spoof = False)

	uno.start()
	# time.sleep(.0001)
	root.after(10)
	# web.start()
	mega.start()
	# run opencv vidcapture in main thread
	# print "Recording {0}, Showing {1}".format(recVar.get(), showVar.get())
	if showVar.get() or recVar.get():
		cap = cv2.VideoCapture(0)
		# first read to get the size
		_, image = cap.read()
		tStart = datetime.now()
		# print cap.get(cv2.cv.CV_CAP_PROP_FPS)
		cv2.waitKey(33)
		_, image = cap.read()
		timeElp = (datetime.now()-tStart).microseconds
		frameRate = 1/(4*timeElp/1e6)
		# print "TIME BETWEEN FRAMES IS {}".format(timeElp/1e6)
		# print "SUGGESTED FPS = {}".format(frameRate)
		if recVar.get() == 1:
			height, width, _ = image.shape
			vid = cv2.VideoWriter()
			suc = vid.open(filename = os.path.join(cfg.userPath,cfg.userFolder, 'CamView.avi'), fourcc = cv2.cv.CV_FOURCC(*'DIVX'), fps = frameRate, frameSize = (width, height))


		while(cfg.recording):
			_, image = cap.read()

			if showVar.get():
				# print image.shape
				cv2.imshow("Webcam View", image)
			if recVar.get():
				vid.write(image)
			# time.sleep(0.011)
			cv2.waitKey(1)
		# vid.close()

		cap.release()
		cv2.destroyWindow("Webcam View")


	# debug printing TODO: dummy out, and set spoof to False
	# print "RECORDING NOW AT"
	# print time.localtime()
	uno.join()
	mega.join()
	# print "FINISHING RECORDING"
	# print time.localtime()
	cameraInstructions(choice = 0)
	return
'''File prompts for video files to be processed
   0 = option 0- initial just copy and process to be used as ground truth/funsies
   1- option 1 - review existing attempt.  prob wont be used
   2- option 2- record new attempt.  copy, process, compare as ground truth
'''
def cameraInstructions(choice = 0):
	ohPath = Tkinter.StringVar()
	sidePath = Tkinter.StringVar()
	# frontPath = Tkinter.StringVar()
	def setOH():
		ohPath.set(tkFileDialog.askopenfilename(defaultextension = '.avi'))
		return
	def setSide():
		sidePath.set(tkFileDialog.askopenfilename(defaultextension = '.avi'))
		return

	tkMessageBox.showinfo("Instructions for Camera Access", "Plug in camera USB hub and select Overhead, and Side video files respectively")
	clearOut(root)
	camFrame = Tkinter.Frame(root).grid()
	# list of labels and textentries with buttons next to them for files
	ohLabel = Tkinter.Label(camFrame, text ="Overhead View File").grid(row = 1, column = 0)
	ohEntry = Tkinter.Label(camFrame, textvariable = ohPath, relief = Tkinter.SUNKEN).grid(row =2, column = 0)
	ohButton = Tkinter.Button(camFrame, text = "...", command = setOH).grid(row = 2, column = 1)	
	
	sideLabel = Tkinter.Label(camFrame, text ="Side View File").grid(row = 3, column = 0)
	sideEntry = Tkinter.Label(camFrame, textvariable = sidePath, relief = Tkinter.SUNKEN).grid(row =4, column = 0)
	sideButton = Tkinter.Button(camFrame, text = "...", command = setSide).grid(row = 4, column = 1)	

	# frontLabel = Tkinter.Label(camFrame, text ="Front View File").grid(row = 5, column = 0)
	# frontEntry = Tkinter.Label(camFrame, textvariable = frontPath, relief = Tkinter.SUNKEN).grid(row =6, column = 0)
	# frontButton = Tkinter.Button(camFrame, text = "...", command = setFront).grid(row = 6, column = 1)	
	


	def continueProcess0():
		# TODO: check option choice, and based on that decide to process alone or correlate with ground truth
		if os.path.isfile(sidePath.get()) and os.path.isfile(ohpath.get()):
			cfg.userHeights = img.sideProcess(sidePath.get())
			cfg.userAngles = img.ohProcess(ohPath.get())
			shutil.copy2(sidePath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi'))
			shutil.copy2(ohPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi'))
			# shutil.copy2(frontPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'frontView.avi'))
			# create analysis images, and go to screen to present them- maybe have message box saying where everything is saved
			perf.wholeShebang(alone = True)
			# move onto window that nicely shows images
			showResults()
		else:
			tkMessageBox.showinfo("ERROR", "Invalid files, try again")
			return;

	def continueProcess2():
		# TODO: check option choice, and based on that decide to process alone or correlate with ground truth
		if os.path.isfile(sidePath.get()) and os.path.isfile(ohpath.get()):

			shutil.copy2(sidePath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi'))
			shutil.copy2(ohPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi'))
			tkMessageBox.showinfo("Video copying completed", "Will now process the videos. This could take a while")
			cfg.userHeights = img.sideProcess(sidePath.get())
			cfg.userAngles = img.ohProcess(ohPath.get())
			# shutil.copy2(frontPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'frontView.avi'))
			# create analysis images, and go to screen to present them- maybe have message box saying where everything is saved
			perf.wholeShebang(alone = False)
			# move onto window that nicely shows images
			showResults()
		else:
			tkMessageBox.showinfo("ERROR", "Invalid files, try again")
			return;
	def skipProcess0():
		tkMessageBox.showinfo("Video Selection Skipped", "Will show just the sensor data")
		showResults(compared = False)
		copied = False
		if os.path.isfile(sidePath.get()):
			shutil.copy2(sidePath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi'))
			copied = True
		if os.path.isfile(ohPath.get()):
			shutil.copy2(ohPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi'))
			copied = True
		if copied:
			tkMessageBox.showinfo("Videos Copied", "You selected video files anyway, so we will copy them in and just not analyze for now")
		else:
			tkMessageBox.showinfo("Video Selection Skipped", "Will show just the sensor data")
	def skipProcess2():

		copied = False
		if os.path.isfile(sidePath.get()):
			shutil.copy2(sidePath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi'))
			copied = True
		if os.path.isfile(ohPath.get()):
			shutil.copy2(ohPath.get(), os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi'))
			copied = True
		if copied:
			tkMessageBox.showinfo("Videos Copied", "You selected video files anyway, so we will copy them in and just not analyze for now")
		else:
			tkMessageBox.showinfo("Video Selection Skipped", "Will show just the sensor data")

		showResults(compared = True)		
	if choice ==0:
		nextButton = Tkinter.Button(camFrame, text = "Continue", command = continueProcess0).grid(row =3, column =5)
		skipButton = Tkinter.Button(camFrame, text = "SKIP", command = skipProcess0)
		skipButton.grid(row =4, column = 5)
	elif choice == 2:
		nextButton = Tkinter.Button(camFrame, text = "Continue", command = continueProcess2).grid(row =3, column =5)	
		skipButton = Tkinter.Button(camFrame, text = "SKIP", command = skipProcess2)
		skipButton.grid(row =4, column = 5)	
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
	user = Tkinter.StringVar()
	user.set(' ')
	gtpath.set(' ')
	def setGTPath():
		gtpath.set(tkFileDialog.askdirectory(parent = root))
		cfg.gtPath = gtpath.get()
	def setUserPathFold():
	
		temp = tkFileDialog.askdirectory(parent = root)
		cfg.userPath = os.path.split(temp)[0]
		cfg.userFolder = os.path.split(temp)[1]
		# TODO delete this
		print os.path.split(temp)
		userpath.set(cfg.userPath)
		nameFolder.set(cfg.userFolder)
		user.set(os.path.join(cfg.userPath, cfg.userFolder))
	clearOut(root)
	frame1 = Tkinter.Frame(root)
	frame1.grid()
	userLabel = Tkinter.Label(frame1, text = "User Folder")
	gtLabel = Tkinter.Label(frame1, text = "Name of Example/Folder")
	gtLabel.grid(row = 0,column = 0)
	userLabel.grid(row = 1, column = 0)
	name = Tkinter.Label(frame1, textvariable = user,relief = Tkinter.SUNKEN, width = 50)
	name.grid(row = 1, column =1)
	gt = Tkinter.Label(frame1, textvariable = gtpath, relief = Tkinter.SUNKEN, width = 50)
	gt.grid( row = 0, column = 1)
	userButton = Tkinter.Button(frame1, text = '...', command = setUserPathFold)
	userButton.grid(row =1, column = 2)
	gtButton = Tkinter.Button(frame1, text = '...', command = setGTPath)
	gtButton.grid(row = 0, column =2)

	# checkbutton for skipping ground truth
	def toggleSkip():
		if skipGrade.get():
			# make the ground truth things have no state
			gtButton.config(state = Tkinter.DISABLED)
			gtpath.set('--------')

		else:
			gtButton.config(state=Tkinter.NORMAL)
			gtpath.set('')
	skipGT = Tkinter.Checkbutton(frame1, text = "Skip Ground Truth Analysis ", variable = skipGrade, command = toggleSkip)
	skipGT.grid(row = 0, column = 5)


	backButton = Tkinter.Button(frame1, text = "BACK", command = viewInit)
	startButton = Tkinter.Button(frame1, text = "START", command = option1_start)
	backButton.grid(row = 0, column = 10)
	startButton.grid(row = 1, column = 10)

	padWidgets(frame1)

def option1_start():
	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, 'data.mat')):
		cfg.loadUserData()
	else:
		tkMessageBox.showinfo('ERROR', 'No data.mat file found in user folder')
		return
	if os.path.isfile(os.path.join(cfg.gtPath, 'data.mat')) and not skipGT.get():
		cfg.loadGT()
	else:
		tkMessageBox.showinfo('ERROR', 'No data.mat file found in GT folder')
		return	
	# check if there is data first, so we dont have to run video processing again

	perf.wholeShebang(alone = skipGT.get())	
	showResults()
	

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
	xScroll = Tkinter.Scrollbar(frame2, orient = Tkinter.HORIZONTAL).grid(row = 11)

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


	recCheck = Tkinter.Checkbutton(frame2, text = "Record With Webcam", variable = recVar)
	showCheck = Tkinter.Checkbutton(frame2, text = "Show Webcam View While Playing", variable = showVar)
	recCheck.grid(row = 0, column = 3)
	showCheck.grid(row = 1, column = 3)
	homeButton = Tkinter.Button(frame2, text = "Back", command = viewInit).grid(row = 0, column = 5)
	resetButton = Tkinter.Button(frame2, text = "Reset", command = reset).grid(row = 1, column = 5)
	
	startButton = Tkinter.Button(frame2, text = "START", command = option2_preStart, bg = 'GREEN').grid(row = 2, column = 5)
	


	padWidgets(frame2)
def option2_preStart():
	# check if os join of path and name folder exists, and if it does, return a message box
	if os.path.isdir(os.path.join(cfg.userPath, nameFolder.get())):

		tkMessageBox.showinfo("ERROR", "Folder already exists! Pick another")
		return
	# check for empty strings
	elif len(nameFolder.get()) ==0  or duration.get() is None or len(userpath.get()) == 0 or cfg.unoPath is '' or cfg.megaPath is '' or cfg.megaPath is cfg.unoPath:
		tkMessageBox.showinfo("ERROR", "Missing data, please fill in everything")
		return
	else:
		clearOut(root)
		frameC = Tkinter.Frame(root)
		frameC.grid()
		countLabel = Tkinter.Label(frameC, text = 3, bg = 'YELLOW', font = ('Helvetica', 72))
		countLabel.grid()
		# option0_start()
		countdown2(3, countLabel)
# open connections with arduino, then move on to find video files
def countdown2(count, label):

	if count <0:
		option2_start()
	else:
		if count is 0:
			label.configure(bg = 'GREEN')
		label.configure(text = count)
		count = count-1
		root.after(1000, countdown, count, label)

def option2_start():
	#TODO: function to pick up/set all appropriate values
	# check if os join of path and name folder exists, and if it does, return a message box
	# if os.path.isdir(os.path.join(cfg.userPath, nameFolder.get())):
	# 	tkMessageBox.showinfo("ERROR", "Folder already exists! Pick another")
	# 	return
	# # check for empty strings
	# elif len(nameFolder.get()) ==0  or duration.get() is None or len(userpath.get()) == 0 or cfg.unoPath is '' or cfg.megaPath is '' or cfg.megaPath is cfg.unoPath:
	# 	tkMessageBox.showinfo("ERROR", "Missing data, please fill in everything")
	# 	return
	cfg.userFolder = nameFolder.get()
	os.mkdir(os.path.join(cfg.userPath, cfg.userFolder))
	clearOut(root)
	frame0A = Tkinter.Frame(root).grid()
	# maybe make a thing that flashes based on tempo in recording adjustment thread? if tempo is set, that is
	nowRecording = Tkinter.Label(frame0A, text = "FINISHED RECORDING", bg = 'YELLOW', font = ('Helvetica', 72)).grid()

	#time.sleep(0.1)
	mega = readHits.megaComm(1, "MegaComm", spoof = True)
	uno = readHits.unoComm(2, "UnoComm", spoof = True)
	uno.start()
	time.sleep(.0001)
	mega.start()
	# debug printing TODO: dummy out, and set spoof to False
	# print "RECORDING NOW AT"
	# print time.localtime()
	if showVar.get() or recVar.get():
		cap = cv2.VideoCapture(0)
		# first read to get the size
		_, image = cap.read()
		# print cap.get(cv2.cv.CV_CAP_PROP_FPS)
		if recVar.get() == 1:
			height, width, _ = image.shape
			vid = cv2.VideoWriter()
			suc = vid.open(filename = os.path.join(cfg.userPath,cfg.userFolder, 'CamView.avi'), fourcc = cv2.cv.CV_FOURCC(*'XVID'), fps = 15, frameSize = (width, height))

        # print "Recording {}".format(cfg.recording)
		while(cfg.recording):
			_, image = cap.read()
			print image.shape
			if showVar.get():
				# print image.shape
				cv2.imshow("Webcam View", image)
			if recVar.get():
				vid.write(image)
			# time.sleep(0.011)
			cv2.waitKey(33)
		# vid.close()

		cap.release()
		cv2.destroyWindow("Webcam View")
	uno.join()
	mega.join()
	# print "FINISHING RECORDING"
	# print time.localtime()
	cameraInstructions(choice = 2)
	pass


''' if i get fluid synth going, make an instrument version
	base window: set mega path and sf2 path
'''
def FUN():
	# sf2 = Tkinter.StringVar()
	def pickSF2():
		sf2.set(tkFileDialog.askopenfilename(defaultextension = '.sf2'))
		cfg.sf2Path = sf2.get()
		return
	def startFun():
		# check that 
		if sf2.get() is None:
			tkMessageBox.showinfo('ERROR', 'Please select a SoundFont file')
		else:
			synthMode()
	clearOut(root)
	funFrame = Tkinter.Frame(root).grid()
	serialList = readHits.serial_ports()
	megaScroll = Tkinter.Scrollbar(funFrame, orient = Tkinter.HORIZONTAL)
	megaScroll.grid(row = 2, column =0, sticky = Tkinter.E+ Tkinter.W)
	megaLabel = Tkinter.Label(funFrame, text = "Address of Mega (Sensor Reader)").grid(row = 1, column = 0)
	megaBox = Tkinter.Listbox(funFrame, selectmode = Tkinter.SINGLE)
	for address in serialList:
		megaBox.insert(Tkinter.END, address)
	megaBox.grid(row = 1, column = 1)	
	megaBox.config(xscrollcommand = megaScroll.set)
	megaScroll.config(command = megaBox.xview)
	def megaSelect(evt):
		cfg.megaPath = megaBox.get(megaBox.curselection())
	megaBox.bind('<<ListboxSelect>>', megaSelect)

	sf2Label = Tkinter.Label(funFrame, textvariable = sf2).grid(row = 3, column = 0)
	sf2Button = Tkinter.Button(funFrame, text = "...", command = pickSF2).grid(row = 3, column = 1)
	startButton = Tkinter.Button(funFrame, text = "To Play Space", command = startFun).grid(row = 0, column = 3)
	backButton = Tkinter.Button(funFrame, text = "BACK", command = viewInit).grid(row = 1, column = 3)

	# print "AWWW YEEAAAHHHH"

''' has start/stop threads, hopefully someday add changing octaves/instruments '''
def synthMode():
	if sf2.get() is "":
		tkMessageBox.showinfo("ERROR", "please select a .sf2 file")
		return
	clearOut(root)
	synthFrame = Tkinter.Frame(root)
	synthFrame.grid()
	# cfg.playing = True
	synth = readHits.megaSynth(1, "SynthComm", spoof = False)
	def setThread():
		cfg.playing = True
		synth.start()
	def stopThread():
		cfg.playing = False
		# check if the synth serial communication was started
		if "SynthComm" in threading.enumerate():
			synth.join()
		FUN()
	def setOctave():
		readHits.octave= octave.get()
	octLabel = Tkinter.Label(synthFrame, text = "Octave").grid(row = 4, column = 0)
	tempoEntry = Tkinter.Spinbox(synthFrame, from_ = 1, to = 8, textvariable = octave, command  = setOctave).grid(row = 5, column = 0)
	

	startButt = Tkinter.Button(synthFrame, text = 'START', command = setThread)
	startButt.grid(row = 0, column = 0)
	backButt = Tkinter.Button(synthFrame, text = 'BACK', command = stopThread)
	backButt.grid(row = 1, column = 0)
''' for showing results '''	
# def showResults(compared):
# 	# print cfg.userHits.shape
# 	# generate grid + canvas in each area
# 	# check that file exists for each, then show
# 	# if not, show question mark bitmap
# 	clearOut(root)
# 	resultFrame = Tkinter.Frame(root)
# 	resultFrame.grid()
# 	qmark = Tkinter.PhotoImage("bin/qmark.png")
# 	#the general sheet music style image
# 	# TODO: make it scrollable
# 	genCanvas = Tkinter.Canvas(resultFrame, bg = 'blue')
# 	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "hitSheet.gif")):
# 		genPic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "hitSheet.gif"))
# 		genCanvas.create_image(0,0,image= genPic)
# 	else: 
# 		genCanvas.create_image(0,0, image = qmark)
# 		pass
# 	genCanvas.grid(row = 0, column = 0)
# 	genScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
# 	genScroll.grid(row = 1, column = 0)
# 	genCanvas.config(xscrollcommand = genScroll.set)
# 	genScroll.config(command = genCanvas.xview)

# 	# locations
# 	locCanvas = Tkinter.Canvas(resultFrame, bg = 'gray')#, width = 400, height = 400)
# 	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "locations.gif")):

# 		locPic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "locations.gif"))
# 		locCanvas.create_image(0,0,image= locPic)
# 	else: 
# 		# make question mark
# 		print "HELLO WORLD"
# 		locCanvas.create_image(0,0, image = qmark)
# 		pass
# 	locCanvas.grid(row = 2, column = 0)
# 	locScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
# 	locScroll.grid(row = 3, column = 0)
# 	locCanvas.config(xscrollcommand = locScroll.set)
# 	locScroll.config(command = locCanvas.xview)
# 	#heights
# 	heightCanvas = Tkinter.Canvas(resultFrame, bg = 'red')
# 	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "heights.gif")):
# 		heightPic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "heights.gif"))
# 		heightCanvas.create_image(0,0,image= heightPic)
# 	else: 
# 		# make question mark
# 		heightCanvas.create_image(0,0,image = qmark)
# 		pass
# 	heightCanvas.grid(row = 2, column = 1)
# 	heightScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
# 	heightScroll.grid(row = 3, column = 1)
# 	heightCanvas.config(xscrollcommand = heightScroll.set)
# 	heightScroll.config(command = heightCanvas.xview)

# 	# angles
# 	angleCanvas = Tkinter.Canvas(resultFrame, bg = 'green')#, width = 400, height = 400)
# 	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "angles.gif")):
# 		anglePic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "angles.gif"))
# 		angleCanvas.create_image(0,0,image= anglePic)
# 	else: 
# 		# make question mark
# 		angleCanvas.create_image(0,0, image = qmark)
# 		pass
# 	angleCanvas.grid(row = 2, column = 2)
# 	angleScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
# 	angleScroll.grid(row = 3, column = 2)
# 	angleCanvas.config(xscrollcommand = angleScroll.set)
# 	angleScroll.config(command = angleCanvas.xview)
# 	#if compared, add text area of results
# 	if compared:
# 		# TODO - text area on midright that shows missed/extra hits, and average error in each thing
# 		pass
# 	#home & quit button
# 	homeButton = Tkinter.Button(resultFrame, text = "HOME", command = viewInit)
# 	quitButton = Tkinter.Button(resultFrame, text = "QUIT", command = quit)
# 	homeButton.grid(row = 0, column = 10)
# 	quitButton.grid(row = 1, column = 10)
''' same as above but using label instead of canvas '''
def showResults(compared):
	# print cfg.userHits.shape
	# generate grid + canvas in each area
	# check that file exists for each, then show
	# if not, show question mark bitmap
	clearOut(root)
	resultFrame = Tkinter.Frame(root)
	resultFrame.grid()
	qmark = Tkinter.PhotoImage("bin/qmark.png")
	#the general sheet music style image
	# TODO: make it scrollable
	genCanvas = Tkinter.Canvas(resultFrame, bg = 'blue')
	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "hitSheet.gif")):
		genPic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "hitSheet.gif"))
		genCanvas.create_image(0,0,image= genPic)
	else: 
		genCanvas.create_image(0,0, image = qmark)
		pass
	genCanvas.grid(row = 0, column = 0)
	genScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
	genScroll.grid(row = 1, column = 0)
	genCanvas.config(xscrollcommand = genScroll.set)
	genScroll.config(command = genCanvas.xview)

	# locations
	locCanvas = Tkinter.Canvas(resultFrame, bg = 'gray')#, width = 400, height = 400)
	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "locations.gif")):

		locPic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "locations.gif"))
		locCanvas.create_image(0,0,image= locPic)
	else: 
		# make question mark
		print "HELLO WORLD"
		locCanvas.create_image(0,0, image = qmark)
		pass
	locCanvas.grid(row = 2, column = 0)
	locScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
	locScroll.grid(row = 3, column = 0)
	locCanvas.config(xscrollcommand = locScroll.set)
	locScroll.config(command = locCanvas.xview)
	#heights
	heightCanvas = Tkinter.Canvas(resultFrame, bg = 'red')
	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "heights.gif")):
		heightPic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "heights.gif"))
		heightCanvas.create_image(0,0,image= heightPic)
	else: 
		# make question mark
		heightCanvas.create_image(0,0,image = qmark)
		pass
	heightCanvas.grid(row = 2, column = 1)
	heightScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
	heightScroll.grid(row = 3, column = 1)
	heightCanvas.config(xscrollcommand = heightScroll.set)
	heightScroll.config(command = heightCanvas.xview)

	# angles
	angleCanvas = Tkinter.Canvas(resultFrame, bg = 'green')#, width = 400, height = 400)
	if os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, "angles.gif")):
		anglePic = Tkinter.PhotoImage(os.path.join(cfg.userPath, cfg.userFolder, "angles.gif"))
		angleCanvas.create_image(0,0,image= anglePic)
	else: 
		# make question mark
		angleCanvas.create_image(0,0, image = qmark)
		pass
	angleCanvas.grid(row = 2, column = 2)
	angleScroll = Tkinter.Scrollbar(resultFrame, orient = Tkinter.HORIZONTAL)
	angleScroll.grid(row = 3, column = 2)
	angleCanvas.config(xscrollcommand = angleScroll.set)
	angleScroll.config(command = angleCanvas.xview)
	#if compared, add text area of results
	if compared:
		# TODO - text area on midright that shows missed/extra hits, and average error in each thing
		pass
	#home & quit button
	homeButton = Tkinter.Button(resultFrame, text = "HOME", command = viewInit)
	quitButton = Tkinter.Button(resultFrame, text = "QUIT", command = quit)
	homeButton.grid(row = 0, column = 10)
	quitButton.grid(row = 1, column = 10)
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
