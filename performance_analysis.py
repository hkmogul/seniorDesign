import numpy as np
import matplotlib.pyplot as plt

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
    else if data.shape[1] > gt.shape[1]:
        pad = np.zeros((3, data.shape[1]-gt.shape[1]))
        gt = np.hstack((gt, pad))
    return gt, data


''' Compares ground truth and data signal, and returns 2 arrays
    One corresponds to errors in ground truths (data stream not signal)
    Other is extra hits
    error = window to check around (default = 10ms)
'''

def grade_perf(gt, data, error =50):
    # DELETE DATA POINTS AS YOU GO
    data_temp = data
    results = np.zeros(gt.shape)
    for i in xrange(10,gt.shape[1]):
        # time = i in milliseconds
        found = False
        foundIn = 0
        # find if there is a signal in the data that is within the error window
        for j in xrange(-1*error, error+1):
            if data_temp[1][i+j] is not 0:
                found = True
                foundIn = i+j
                break
        if found is True:
            timeError = i - foundIn
            velError = gt[1][i] - data_temp[1][foundIn]
            xError = gt[2][i] - data_temp[2][foundIn]
            yError = gt[3][i] - data_temp[3][foundIn]
            # delete data point so it isnt double counted- set to 0 to not mess with timestamps
            data_temp[:][foundIn] = np.zeros()
        else:
            timeError = -15


    return results
