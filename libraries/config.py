''' Configuration and global variables for cross module performance
    Hilary Mogul - hilary.mogul@gmail.com
'''
import numpy as np
import os

# if in recording mode
recording = False

''' session settings '''
duration = 0 # in seconds
tempo = 0 # in bpm
repeating = False # repeating per measure

# meant to be the users hits
userHits = np.empty((4,0))

#user heights- has time and height for each stick - do left, right
userHeights = np.empty((3,0))

userAngles = np.empty((2,0))

#ground truth of what the user should be getting
groundTruth = np.empty((4,0))
# ground truth heights and angles
gtHeights = np.empty((3,0))

gtAngles = np.empty((2,0))



'''color settings (HSV)'''
# lower and upper bounds for tip of Right stick
tipR_lower = np.array([85,140,175])
tipR_upper = np.array([95,200,255])

#lower and upper bounds for band of Right stick
stickR_lower = np.array([0,0,0])
stickR_upper = np.array([0,0,0])


# lower and upper bounds for tip of Left stick
tipL_lower = np.array([7,175,175])
tipL_upper = np.array([15,255,255])

#lower and upper bounds for band of Left stick
stickL_lower = np.array([0,0,0])
stickL_upper = np.array([0,0,0])

''' paths to folders for each '''
userPath = '~/Desktop/UserInfo'
if not os.path.exists(userPath):
    os.mkdir(userPath)
userFolder = '/'

gtPath = '~/Desktop/TeacherInfo'
gtFolder = '/'
if not os.path.exists(gtPath):
    os.mkdir(gtPath)

def setUserPath(name):
    userPath = name
    if not os.path.exists(userPath):
        os.mkdir(userPath)

def setUserFolder(name):
    userFolder = name
    if not os.path.exists(os.path.join(userPath, userFolder)):
        os.mkdir(os.path.join(userPath, userFolder))

def setGTFolder(name):
    gtFolder = name
    if not os.path.exists(os.path.join(gtPath, gtFolder)):
        os.mkdir(os.path.join(gtPath, gtFolder))



def resetUser():
    userHits = np.empty((4,0))
