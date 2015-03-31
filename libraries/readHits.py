''' Functions/scripts for reading hits from arduino
    Hilary Mogul- hilary.mogul@gmail.com
'''

import numpy as np
import time
import datetime
import serial
import threading
import glob
import sys
import config

''' Parse string from arduino serial monitor to return location, velocity,
    time, etc
    Example expected string to parse would be: '01-1056'= northwest velocity = 56
    timeStart should be an int in ms declared
'''
def parseInput(timeStart, input = None):
    if input is None:
        return None
    # get time first to mitigate delays- convert to millis to prevent overflow
    timeDiff = (timeStart - time.time()).microseconds/1000
    x = int(input[:2])
    y = int(input[2:4])
    vel = int(input[-3:])
    return timeDiff, x, y, vel


''' Open a serial connection with arduino, then read until some global variable hits
    Expected to be called upon in a thread, then started/killed when necessary
'''
def openComm(notStore= True):
    timeStart = time.time()
    ser = serial(config.megaPath, config.megaBaud,timeout = 0)
    if notStore:
        # code for print and parse goes here
        while config.recording:
            info = serial.readline()
            if info is not None:
                    time, x, y, vel = parseInput(timeStart, info)
                    print "-----"
                    print "Time: {0} \nPosition: {1},{2}\n Velocity: {3}".format(time, x, y, vel)
                    print "-----"
    else:
        while config.recording:
            info = serial.readline()
            if info is not None:
                time, x, y, vel = parseInput(timeStart, info)
                config.userHits = np.hstack((config.userHits, np.array([[time],[vel],[x],[y])))
    # when done, close out connection
    ser.close()
    return


class megaComm(threading.Thread):
    def __init__(self, threadID, name, notStore = True, spoof = False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.notStore = notStore
        self.spoof = spoof
    def run(self):
        if not self.spoof:
            openComm(notStore = notStore)
class unoComm(threading.Thread):
    def __init__(self, threadID, name, spoof = False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.spoof = spoof
        config.recording = True
    def run(self):
        if not self.spoof:
            comm = serial(config.unoPath, config.unoBaud, timeout = 0)
        # TODO: send message that will start video
        time.sleep(config.duration)
        config.recording = False
        # TODO: send message that will end video
        if not self.spoof:
            comm.close()
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
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
