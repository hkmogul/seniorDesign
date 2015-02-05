import Tkinter
import datetime


class simpleapp_tk(Tkinter.Tk):
    global timerStarted
    def click(event):
        print event.x
        print event.y
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        timerStarted = False
        self.initialize()

    def initialize(self):
        frame = Tkinter.Frame(self, width = 800, height = 600)
        frame.grid()
        frame.bind("<Button-1>", click)
        # global timerStarted
        global startVar
        startVar = Tkinter.StringVar().set(u"START")
        button = Tkinter.Button(self, textvariable = startVar, command = self.hitButton)
        button.grid(column = 1, row = 0)


    def hitButton(event):
        if not timerStarted:
            timerStarted = True
            global startTime
            startTime= datetime.time()
            print startTime.isoformat()
            print "Timer started! Get clickin!"
            startVar.set("STOP")
        else:
            timerStarted = False
            global stopTime
            stopTime = datetime.time()
            startVar.set("START")
if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Poop Emoji Here')
    app.mainloop()
