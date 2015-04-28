import numpy as np
import matplotlib.pyplot as plt
import os
import config as cfg 
import matplotlib.figure as fig
import math
import sys

sys.path.append('libraries')
import imageFunctions as img
# analysis functions for analyzing the output of

''' Utility for turning raw data into signal stream (default resolution = 1ms)
    Basing this off idea that data is 4xN of time, velocity, x, y with time in ms
    And N = number of strikes


'''
def raw2sig(data, length = None, resolution = 1):
    # if unspecified length, make it 100 ms after last strike
    if length is None:
        length = data[0][data.shape[1]-1]+100
    # declare the numpy array of this length
    sig = np.zeros((3,length))

    for i in xrange(data.shape[1]):
        index = data[0][i]
        sig[:][length] = data[1:3][i]

    return sig

''' Utility to make sure two compared signal streams are the same length
    Returns both arrays, the one with a smaller signal
    NOTE: This is for signal streams, not puredata
    gt = ground truth array
    data = collected array
'''
def pad_lesser(gt, data):
    if gt.shape[1] > data.shape[1]:
        pad = np.zeros((3, gt.shape[1]-data.shape[1]))
        data = np.hstack((data, pad))
    elif data.shape[1] > gt.shape[1]:
        pad = np.zeros((3, data.shape[1]-gt.shape[1]))
        gt = np.hstack((gt, pad))
    return gt, data




''' Returns error on each hit from ground truth in 4xN array of error of each
    AKA not time based array
    Missed hit = time error of -1000
    Error argument = window to allow checking for time things around an area
    (in milliseconds)
    gt = ground truth
    userdata= user input
'''
def gradeRef(gt, userdata, error = 50):
    results = np.zeros(gt.shape)
    data = np.copy(userdata)
    found = False
    for i in xrange(gt.shape[1]):
        found = False
        # check error window for a hit in that timeframe (by checking velocity)
        for j in xrange(data.shape[1]):
            if abs(data[0][j] - gt[0][i]) <= error:
                # then its a hit! get errors of each 
                results[0][i] = gt[0][i] - data[0][j]
                results[1][i] = gt[1][i] - data[1][j]
                results[2][i] = gt[2][i] - data[2][j]
                results[3][i] = gt[3][i] - data[3][j]
                found = True
                # delete this hit so its not double counted
                data = np.delete(data, j, 1)
                break;
        if not found:
            results[0][i] = -1000
    # return results and remaining data to denote extra hits
    return results, data
''' make sheet music style printout 
    saves to either CWD (debug = True)
    or to user Path in cfg
    sig = numerator of time signature (how many beats per measure)
'''
def pltGeneral(userdata, gt = None, debug = False, sig = 4):
    plt.clf()
    # length of figure based on # of hits?
    plt.figure(figsize=(24,6), dpi = 80)
    if debug:
        tempo = 120
    else:
        tempo = cfg.tempo
    interval =60000/tempo
    # user = plt.stem(userdata[0], userdata[1])
    user = plt.plot(userdata[0], userdata[1], 'o')
    plt.legend()

    if gt is not None:
        # gt = plt.stem(gt[0], gt[1], linefmt = 'g',markerfmt = 'go')
       gt = plt.plot(gt[0], gt[1], 'go')

    # start making vertical lines
    end = plt.axis()[1] +100
    plt.axis([0,end, 0,127])
    ymax = plt.axis()[3]
    plt.xlabel("Time (ms)")
    plt.ylabel("Velocity (MIDI Style)")
    vRange = np.arange(0,end, interval)
    mesRange = np.arange(0,end,interval*sig)
    plt.vlines(vRange, 0, 127, linestyles = 'dashed')
    plt.vlines(mesRange, 0 ,127)

    if debug:
        plt.savefig('hitSheet.gif')
    else:
        plt.savefig(os.path.join(cfg.userpath, 'hitSheet.gif'))
    return
''' scatterplot of positions
TODO: size of points based on # of hits
 '''
def pltLocations(userdata, gt = None, debug = False):
    plt.clf()
    x = [-1,0,1,-1,0,1,-1,0,1]
    y = [1,1,1,0,0,0,-1,-1,-1]
    scale = math.fabs(-500*math.atan(userdata.shape[1]+3000)+600)
    # user = plt.scatter(userdata[2], userdata[3])
    userAmt = positionAmts(userdata)
    userSize = userAmt*int(scale)
    # userSize = np.power(userAmt,2) * int(-1*math.atan(userdata.shape[1]/3-100)+11.5)
    print "Scale : {}".format(scale)
    print "User size : {}".format(userSize)
    # userSize = [20*2**n for n in range(len(userAmt))]
    user = plt.scatter(x,y,s = userSize, color = '#ff6600',alpha=0.5)
    if gt is not None:
        gtAmt = positionAmts(gt)
        # gtSize = np.power(gtAmt, 3)/50 * int(-1*math.atan(userdata.shape[1]/3-100)+11.5)
        gtSize = gtAmt*int(scale)
        # gtSize = 
        # gtSize = [20*2**n for n in range(len(gtAmt))]
        print "gtSize: {}".format(gtSize)

        gt = plt.scatter(x, y, s= gtSize, c = u'b', alpha = 0.5)
    plt.axis([-2,2,-2,2])
    if debug:
        plt.savefig('locations.gif')
    else:
        plt.savefig(os.path.join(cfg.userpath, 'locations.gif'))
    return

def sizePlot():
    x = np.arange(-5000,5000)
    # print x[4995:5005]
    scale = -10*(np.arctan(x*.001))
    print np.amax(scale)
    print scale[4995:5005]
    plt.plot(x,scale)
    plt.savefig('scale.gif')

''' heights vs time '''
def pltHeights(userdata, gt = None, debug = False):
    plt.clf()
    user = plt.plot(userdata[0], userdata[1])
    if gt is not None:
        gtdata = plt.plot(gt[0],gt[1], 'g')
    if debug:
        plt.savefig('heights.gif')
    else:
        plt.savefig(os.path.join(cfg.userpath, 'heights.gif'))
    return
''' angles vs time '''
def pltAngles(userdata, gt= None, debug = False):
    plt.clf()
    user = plt.plot(userdata[0], userdata[1])
    if gt is not None:
        gtdata = plt.plot(gt[0],gt[1], 'g')
    if debug:
        plt.savefig('angles.gif')
    else:
        plt.savefig(os.path.join(cfg.userpath, 'angles.gif'))
    return

''' faster inline function for checking empty hit array '''
def empty(mat):
    return mat.shape[1] is 0

''' Does all images using global files
    alone = True if not compared to GT
 '''
def wholeShebang(alone):
    if alone:
        if not empty(cfg.userHits):
            pltGeneral(cfg.userHits)
            pltLocations(cfg.userHits)
        # check if matrices are empty.  if theyre not, just have to make the images
        if not empty(cfg.userHeights):
            pltHeights(cfg.userHeights)
        elif os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi')):
            img.sideProcess(os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi'))
            pltHeights(cfg.userHeights)

        if not empty(cfg.userAngles):
            pltAngles(cfg.userAngles)
        elif os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi')):
            img.ohProcess(os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi'))
            pltAngles(cfg.userAngles)

    else:
        if not empty(cfg.groundTruth) and not empty(cfg.userHits):
            cfg.error, cfg.extra = perf.gradeRef(cfg.groundTruth, cfg.userHits)
            pltGeneral(cfg.userHits, cfg.groundTruth)
            pltLocations(cfg.userHits, cfg.groundTruth)
        if not empty(cfg.gtHeights) and not empty(cfg.userHeights):
            pltHeights(cfg.userHeights, cfg.gtHeights)
        elif os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi')) and not empty(cfg.gtHeights):
            img.sideProcess(os.path.join(cfg.userPath, cfg.userFolder, 'sideView.avi'))
            pltHeights(cfg.userHeights, cfg.gtHeights)
        if not empty(cfg.gtAngles, cfg.userAngles):
            pltAngles(cfg.userAngles, cfg.gtAngles)
        elif os.path.isfile(os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi')) and not empty(cfg.gtAngles):
            img.ohProcess(os.path.join(cfg.userPath, cfg.userFolder, 'overheadView.avi'))
            pltAngles(cfg.userAngles, cfg.gtAngles)
       


''' better "where" function for finding actual locations
    returns amount of hits of a position given
 '''
def dblWhere(data, x,y):
    m = data[2:5] == np.array([[x],[y]])
    # print "m is {}".format(m)
    n = np.logical_and(m[0], m[1])
    # print "n is {}".format(n)
    return np.sum(n)
''' returns length 9 vector corresponding to amount of hits in each locations

'''
def positionAmts(data):
    amt = np.zeros((9,))
    # print dblWhere(data, -1,1)
    amt[0] = dblWhere(data,-1,1)
    amt[1] = dblWhere(data,0,1)
    amt[2] = dblWhere(data,1,1)
    amt[3] = dblWhere(data,-1,0)
    amt[4] = dblWhere(data,0,0)
    amt[5] = dblWhere(data,1,0)
    amt[6] = dblWhere(data,-1,-1)
    amt[7] = dblWhere(data,0,-1)
    amt[8] = dblWhere(data,1,-1)
    return amt