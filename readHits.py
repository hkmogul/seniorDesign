''' Functions/scripts for reading hits from arduino
    Hilary Mogul- hilary.mogul@gmail.com
'''

import numpy as np
import datetime
import serial

''' Parse string from arduino serial monitor to return location, velocity,
    time, etc
    Example expected string to parse would be: 'NE056'
    timeStart should be an int in ms declared
'''
def parseInput(input = None, timeStart):
    if input is None:
        return None
    # get time first to mitigate delays
    t =
    loc = input[:2]
    
