''' Configuration and global variables for cross module performance
    Hilary Mogul - hilary.mogul@gmail.com
'''
import numpy as np
import os
import scipy.io
# if in recording mode
recording = False
playing = False
''' session settings '''
duration = 0 # in seconds
tempo = 120 # in bpm
sig = 4 # numerator of time signature
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

error = np.empty((4,0)) #errors in hits
extra = np.empty((4,0)) # extra hits

'''color settings (HSV)'''
# lower and upper bounds for tip of Right stick
# tipR_lower = np.array([170,100,75])
# tipR_upper = np.array([179,255,255])
# BRIGHT YELLOW GAFF
# orig hsv 42, 192, 198
tipR_lower = np.array([27,50,100])
tipR_upper = np.array([52,255,255])


#lower and upper bounds for band of Right stick
# GREEN GAFF- 69, 165, 191
stickR_lower = np.array([65,100,150])
stickR_upper = np.array([100,255,255])


# lower and upper bounds for tip of Left stick
# PINK- 161,164,255
tipL_lower = np.array([140,40,200])
tipL_upper = np.array([170,240,255])
#lower and upper bounds for band of Left stick
# ORANGE - 2, 184, 252
stickL_lower = np.array([1,155,155])
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
megaBaud = 19200

''' path of sf2 file for synthesizing '''
sf2Path = ''
octave = 1
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

''' load user data from .mat file.  useful for option1 '''
def loadUserData():
    if os.path.isfile(os.path.join(userPath, userFolder, 'data.mat')):
        mat_contents = scipy.io.loadmat(os.path.join(userPath, userFolder, 'data.mat'))
        userHeights = mat_contents['heights']
        userAngles = mat_contents['angles']
        userHits = mat_contents['hits']
        tempo = mat_contents['tempo']
        duration = mat_contents['duration']
        if 'error' in mat_contents:
            error = mat_contents['error']
            extra = mat_contents['extra']

def saveData():
    name = os.path.join(userPath, userFolder, 'data.mat')
    if extra.shape[1] is not 0 and error.shape[1] is not 0:
        m_dict = {'heights': userHeights, 'angles': userAngles, 'hits': userHits, 'tempo': tempo, 'duration': duration, 'extra': extra, 'error': error}
    else:
        m_dict = {'heights': userHeights, 'angles': userAngles, 'hits': userHits, 'tempo': tempo, 'duration': duration}

    scipy.io.savemat(name, m_dict)
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

    extra = np.empty((4,0))
    error = np.empty((4,0))
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
