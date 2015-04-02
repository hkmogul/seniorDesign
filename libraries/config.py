''' Configuration and global variables for cross module performance
    Hilary Mogul - hilary.mogul@gmail.com
'''
import numpy as np
import os
import scipy.io
# if in recording mode
recording = False

''' session settings '''
duration = 0 # in seconds
tempo = 120 # in bpm
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
# tipR_lower = np.array([170,100,75])
# tipR_upper = np.array([179,255,255])
# BRIGHT YELLOW GAFF
# orig hsv 42, 192, 198
tipR_lower = np.array([30,75,150])
tipR_upper = np.array([45,255,255])


#lower and upper bounds for band of Right stick
# GREEN GAFF- 69, 165, 191
stickR_lower = np.array([60,70,150])
stickR_upper = np.array([85,255,255])


# lower and upper bounds for tip of Left stick
# PINK- 161,164,255
tipL_lower = np.array([150,60,200])
tipL_upper = np.array([167,200,255])
#lower and upper bounds for band of Left stick
# ORANGE - 2, 184, 252
stickL_lower = np.array([0,155,155])
stickL_upper = np.array([8,255,255])

ptsThresh = 250
''' paths to folders for each '''
userPath = ''
#if not os.path.exists(userPath):
 #   os.mkdir(userPath)
userFolder = ''
''' GT PATH SHOULD ALSO INCLUDE THE FOLDER '''
gtPath = ''
#if not os.path.exists(gtPath):
 #   os.mkdir(gtPath)

'''Arduino Paths and Baud rates'''
unoPath = ''
megaPath = ''
unoBaud = 9600
megaBaud = 9600
''' loadmat of values from gt.  returns true if successful '''
def loadGT():
    if os.path.isfile(os.path.join(gtPath, 'data.mat')):
        mat_contents = scipy.io.loadmat(os.path.join(gtPath, 'data.mat'))
        gtHeights = mat_contents['heights']
        gtAngles = mat_contents['angles']
        groundTruth = mat_contents['hits']
        tempo = mat_contents['tempo']
        duration = mat_contents['duration']
        return True 
    else:
        return False
def setUserPath(name):
    userPath = name
    if not os.path.exists(userPath):
        os.mkdir(userPath)

def setUserFolder(name):
    userFolder = name
    if not os.path.exists(os.path.join(userPath, userFolder)):
        os.mkdir(os.path.join(userPath, userFolder))


''' Check if a folder path already exists '''
def checkFolderExists(name):
    pass

def resetUser():
    userHits = np.empty((4,0))

def resetAll():
    recording = False

    ''' session settings '''
    duration = 0 # in seconds
    tempo = 120 # in bpm
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
    ptsThresh = 250
    ''' paths to folders for each '''
    userPath = ''
    #if not os.path.exists(userPath):
     #   os.mkdir(userPath)
    userFolder = ''

    gtPath = ''
    #if not os.path.exists(gtPath):
     #   os.mkdir(gtPath)
