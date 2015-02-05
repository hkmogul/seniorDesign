import Tkinter
from datetime import datetime
import numpy as np


class simpleapp_tk(Tkinter.Tk):
    # hitStack = np.empty([0,4])
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        timerStarted = False
        # global hitStack
        global startTime
        self.initialize()
    def click(event, event1):
        nowTime= datetime.now()
        vel = 50
        print "Position: {0}, {1} \nDelta Time: {2} \n ".format(event1.x, event1.y, (nowTime-startTime))
        # hitStack = np.vstack((hitStack, np.array([(startTime-nowTime), 50,event1.x, event1.y])))
        # print hitStack.shape



    def initialize(self):
        frame = Tkinter.Frame(self, width = 800, height = 600, bg = "dim gray")
        frame.grid()
        frame.bind("<Button-1>", self.click)
        # startTime = datetime.now().microsecond
        print "Timer started at: {0}".format(startTime)
        # startVar = Tkinter.StringVar().set(u"START")
        # button = Tkinter.Button(self, textvariable = startVar, command = self.hitButton)
        # button.grid(column = 1, row = 0)


    # def hitButton(event):
    #     if not timerStarted:
    #         timerStarted = True
    #         global startTime
    #         startTime= datetime.time()
    #         print startTime.isoformat()
    #         print "Timer started! Get clickin!"
    #         startVar.set("STOP")
    #     else:
    #         timerStarted = False
    #         global stopTime
    #         stopTime = datetime.time()
    #         startVar.set("START")
if __name__ == "__main__":
    global startTime
    global hitStack
    startTime = datetime.now()
    # hitStack = np.empty([0,4])
    # print hitStack.shape
    app = simpleapp_tk(None)
    app.title('Poop Emoji Here')
    app.mainloop()
