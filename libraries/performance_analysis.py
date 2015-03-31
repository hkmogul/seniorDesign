import numpy as np
import matplotlib.pyplot as plt
import os
import config
import matplotlib.figure as fig

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

#
# ''' Compares ground truth and data signal, and returns 2 arrays
#     One corresponds to errors in ground truths (data stream not signal)
#     Other is extra hits
#     error = window to check around (default = 10ms)
# '''
#
# def grade_perf(gt, data, error =50):
#     # DELETE DATA POINTS AS YOU GO
#     data_temp = data
#     results = np.zeros(gt.shape)
#     for i in xrange(10,gt.shape[1]):
#         # time = i in milliseconds
#         found = False
#         foundIn = 0
#         # find if there is a signal in the data that is within the error window
#         for j in xrange(-1*error, error+1):
#             if data_temp[1][i+j] is not 0:
#                 found = True
#                 foundIn = i+j
#                 break
#         if found is True:
#             timeError = i - foundIn
#             velError = gt[1][i] - data_temp[1][foundIn]
#             xError = gt[2][i] - data_temp[2][foundIn]
#             # yError = gt[3][i] - data_temp[3][foundIn]
#             # delete data point so it isnt double counted- set to 0 to not mess with timestamps
#             data_temp[:][foundIn] = np.zeros()
#         else:
#             timeError = -15
#
#     results =
#     return results


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
    or to user Path in config
    sig = numerator of time signature (how many beats per measure)
'''
def pltGeneral(userdata, gt = None, debug = False, sig = 4):
    plt.clf()
    plt.figure(figsize=(24,6), dpi = 80)
    if debug:
        tempo = 120
    else:
        tempo = config.tempo
    interval =60000/tempo
    # user = plt.stem(userdata[0], userdata[1])
    user = plt.plot(userdata[0], userdata[1], 'o')

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
    mesRange = np.arange(0,end,interval*4)
    plt.vlines(vRange, 0, 127, linestyles = 'dashed')
    plt.vlines(mesRange, 0 ,127)

    if debug:
        plt.savefig('hitSheet.gif')
    else:
        plt.savefig(os.path.join(config.userpath, 'hitSheet.gif'))
    return
''' scatterplot of positions
TODO: maybe histogram instead? is there such a thing as a 2D histogram?
 '''
# def pltLocations(userdata, gt = None, debug = False):
#     plt.clf()
#     user = plt.scatter(userdata[2], userdata[3])
#     if gt is not None:
#         gt = plt.scatter(gt[2], gt[3], c = u'g')
#     plt.axis([-2,2,-2,2])
#     if debug:
#         plt.savefig('locations.png')
#     else:
#         plt.savefig(os.path.join(config.userpath, 'locations.png'))
#     return
def pltLocations(userdata, gt = None, debug = False):
    plt.clf()
    plt.subplot(211)
    userX = plt.hist(userdata[2], bins = 5)
    if gt is not None:
        gtX = plt.hist(gt[2], bins = 5)
    plt.subplot(212)
    userY = plt.hist(userdata[3], bins = 5)
    if gt is not None:
        gtY = plt.hist(gt[3], bins = 5)
    if debug:
        plt.savefig('locations.gif')
    else:
        plt.savefig(os.path.join(config.userpath, 'locations.gif'))
    return

''' heights vs time '''
def pltHeights(userdata, gt = None, debug = False):
    plt.clf()
    user = plt.plot(userdata[0], userdata[1])
    if gt is not None:
        gtdata = plt.plot(gt[0],gt[1], 'g')
    if debug:
        plt.savefig('heights.gif')
    else:
        plt.savefig(os.path.join(config.userpath, 'heights.gif'))
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
        plt.savefig(os.path.join(config.userpath, 'angles.gif'))
    return








