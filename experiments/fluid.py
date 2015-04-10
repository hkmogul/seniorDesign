''' tester for mingus fluidsynth '''

from mingus.midi import fluidsynth
from mingus.containers import Note
import sys
import time
import random

fluidsynth.init("../HS_Magic_Techno_Drums.SF2")
names = ['A', 'Bb', 'B', 'C', 'Db','D','Eb', 'E', 'F', 'Gb','G','Ab']
# while(True):
# 	n = Note(names[random.randrange(0,11,1)], random.randrange(1,4,1))
# 	n.velocity = random.randrange(40,100,1)
# 	# fluidsynth.set_instrument(1, random.randrange(1,5,1), bank =1)
# 	fluidsynth.play_Note(n)
# 	time.sleep(.1*random.randrange(1,15,1))
# 	# fluidsynth.stop_Note(n)
# 	time.sleep(.5*random.randrange(1,15,1))
# 	# fluidsynth.play_Note(n)

for i in xrange(0,12):
	# for j in xrange(1,4):
	# 	n = Note(names[i],j)
	# 	fluidsynth.play_Note(n)
	# 	time.sleep(2)
	n = Note(names[i], 4)
	n.velocity = 127
	fluidsynth.play_Note(n)
	time.sleep(1)