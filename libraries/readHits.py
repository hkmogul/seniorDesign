''' Functions/scripts for reading hits from arduino
    Hilary Mogul- hilary.mogul@gmail.com
'''

import numpy as np
import time
from datetime import datetime
import serial
import threading
import glob
import sys
from mingus.midi import fluidsynth
import config
from mingus.containers import Note

octave = 4
names = ['C','D','E','F','G','A','B','C','E']
''' Parse string from arduino serial monitor to return location, velocity,
    time, etc
    Example expected string to parse would be: '01-1056'= northwest velocity = 56
    timeStart should be an int in ms declared
'''
def parseInput(timeStart, input = None):
    if input is '':
        return None
    print input
    # get time first to mitigate delays- convert to millis to prevent overflow
    # timeDiff = (timeStart - time.time()).microseconds/1000
    # print time.time()
    timeDiff = (time.time()-timeStart)
    # print input
    x = int(input[:2])

    y = int(input[2:4])
    vel = int(input[4:])
    return timeDiff, x, y, vel


''' Open a serial connection with arduino, then read until some global variable hits
    Expected to be called upon in a thread, then started/killed when necessary
'''
def openComm(notStore= True):
    timeStart = time.time()
    ser = serial.Serial(config.megaPath, config.megaBaud,timeout = 1)
    if notStore:
        # code for print and parse goes here
        while config.recording:
            info = ser.readline()
            if info is not '':
                    timeElp, x, y, vel = parseInput(timeStart, info)
                    print "-----"
                    print "Time: {0} \nPosition: {1},{2}\n Velocity: {3}".format(timeElp, x, y, vel)
                    print "-----"
    else:
        while config.recording:
            info = ser.readline()
            if info is not '':
                timeElp, x, y, vel = parseInput(timeStart, info)
                newHit = np.array([[timeElp], [vel], [x], [y]])
                config.userHits = np.hstack((config.userHits, newHit))
    # when done, close out connection
    ser.close()
    return
''' Return number (0 indexed) of sensor '''
def pos2Num(x,y):
    if y == 1:
        return x+1
    elif y == 0:
        return x+4
    else:
        return x+7
def synthComm():
    # print "I AM IN synthComm"
    timeStart = time.time()
    fluidsynth.init(config.sf2Path)

    note = Note()
    ser = serial.Serial(config.megaPath, config.megaBaud,timeout = 1)
    fluidsynth.stop_Note(note)
    while config.playing:
        info = ser.readline()
        print info
        if info is not '' and len(info) == 9:
            # print info
            # print timeStart
            fluidsynth.stop_Note(note)
            # print "---"
            # print len(info)
            # print "---"

            timeElp, x, y, vel = parseInput(timeStart, info)
            n = pos2Num(x,y)
            # print n
            # print names[n]
            note = Note(names[n],octave)
            note.velocity = vel
            fluidsynth.play_Note(note)

            print "-----"
            print "Time: {0} \nPosition: {1},{2}\n Velocity: {3}".format(timeElp, x, y, vel)
            print "-----"
        else:
            fluidsynth.stop_Note(note)

                # config.userHits = np.hstack((config.userHits, np.array([[time],[vel],[x],[y])))
    # when done, close out connection
    ser.close()
    # print " I HAVE CLOSED THE connection"
    return

class megaSynth(threading.Thread):
    def __init__(self, threadID, name, notStore = True, spoof = False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.notStore = notStore
        self.spoof = spoof
        print "HELLO WORLD I AM INSTANTIATED"
    def run(self):
        if not self.spoof:
            print "HELLO WORLD I RUN NOWs"
            synthComm()
class megaComm(threading.Thread):
    def __init__(self, threadID, name, notStore = True, spoof = False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.notStore = notStore
        self.spoof = spoof
    def run(self):
        if not self.spoof:
            openComm(notStore = self.notStore)
class unoComm(threading.Thread):
    def __init__(self, threadID, name, spoof = False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.spoof = spoof
        config.recording = True
    def run(self):
        if not self.spoof:
            # print "GOING TO PRINT"
            interval = int(60E3/config.tempo)
            # print "W{0}".format(interval)

            time.sleep(0.01) 
            comm = serial.Serial(config.unoPath, config.unoBaud, timeout = 1)
            # set up a loop to wait for arduino to reboot
            temp = None
            while not temp:
                temp = comm.readline()
            # print temp
            # print comm.name
            # comm.write("W{0}\n\n".format(interval))
            # comm.write("{}\n".format(config.tempo))
            comm.write('W {0} {1}\n'.format(int(interval/255),int(interval%255)))
            # comm.write("{}\n".format(int(interval/255)))
            # comm.write("{}\n".format(int(interval%255)))
            tStart = time.time()
            timeElp = time.time()- tStart
            while(timeElp <= config.duration):
                timeElp = time.time() -tStart
                # print timeElp
                info = comm.readline()
                # print info
        # time.sleep(config.duration)
        config.recording = False

        if not self.spoof:
            print "STOPPING RECORDING"
            # comm.write("{0}\n\n".format(interval))
            # comm.write("{}\n".format(config.tempo))
            comm.write('W ')
            # set interval back to 5000 = 19*255 + 255
            comm.write("{} ".format(19))
            comm.write("{} \n".format(155))
            comm.close()

''' find indices of defaults for uno and mega- uno ends in 51, mega ends in 11 '''
def defaults(mylist):
    uno = -1
    foundUno = False
    mega = -1
    foundMega = False
    for index, port in enumerate(mylist):
        if port[-2:] is '51' and not foundUno:
            uno = index
        elif port[-2:] is '11' and not foundMega:
            mega = index
        if foundUno and foundMega:
            break
    return uno, mega

''' I didnt write this, but its really useful '''
def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            # if "Bluetooth" in port:
            #     continue
            # s = serial.Serial(port)
            # s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
