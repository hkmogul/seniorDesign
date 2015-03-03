''' Functions/scripts for reading hits from arduino
    Hilary Mogul- hilary.mogul@gmail.com
'''

import numpy as np
import time
import datetime
import serial

''' Parse string from arduino serial monitor to return location, velocity,
    time, etc
    Example expected string to parse would be: 'NE056'= northeast velocity = 56
    timeStart should be an int in ms declared
'''
def parseInput(input = None, timeStart):
    if input is None:
        return None
    # get time first to mitigate delays
    timeDiff = (timeStart - time.time()).
    loc = input[:2]


''' Open a serial connection with arduino, then read until some global variable hits
    Expected to be called upon in a thread, then started/killed when necessary
'''
def openComm(address = None, baud = None, hitStack = None):
    if address is None:
        ser = serial('/dev/tty.usbmodem1411', 9600)
    else:
        ser = serial(address, baud)
    # TODO: how does this pass values out?, input argument of numpy array?
    if hitStack is None:
        # code for print and parse goes here
    else:
        global hitStack
        
