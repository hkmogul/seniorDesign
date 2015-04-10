''' Tester for performance analysis library '''
import os
import sys
import numpy as np 
import random
sys.path.append('../libraries')
import performance_analysis as perf 

userData = np.empty((4,0))
gtData = np.empty((4,0))
random.seed()
for i in xrange(1,501):
	userData = np.hstack((userData, np.array([[int(i*100*random.uniform(1.,1.5))],[int(60*random.uniform(1.,1.5))],[random.randrange(-1,1,1)],[random.randrange(-1,1,1)]])))
	if i != 3:
		gtData = np.hstack((gtData, np.array([[int(i*100*random.uniform(1.,1.5))],[int(60*random.uniform(1.,1.5))],[random.randrange(-1,1,1)],[random.randrange(-1,1,1)]])))

gtData = np.hstack((gtData, np.array([[400],[60],[1],[1]])))

# print gtData.shape
# print userData
print "---"
# print np.array([[-1],[-1]])
# print userData
# print userData[2:5]
print perf.positionAmts(userData)
print perf.positionAmts(gtData)
results, extra = perf.gradeRef(gtData, userData, error = 49)

print "MISSED HIT AMOUNT"
print np.where(results[0] == -1000)[0].shape[0]

print "EXTRA HITS MADE"
print extra.shape[1]

perf.pltGeneral(userData, gtData, debug = True)
print perf.positionAmts(userData)
print perf.positionAmts(gtData)
perf.pltLocations(userData, gtData, debug = True)
# perf.pltLocations(userData, debug = True)