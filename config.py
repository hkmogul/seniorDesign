''' Configuration and global variables for cross module performance
    Hilary Mogul - hilary.mogul@gmail.com
'''
import numpy as np

# if in recording mode
recording = False

# meant to be the users hits
userHits = np.empty((4,0))

groundTruth = np.empty((4,0))


def resetUser():
    userHits = np.empty((4,0))
