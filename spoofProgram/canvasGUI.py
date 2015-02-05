import Tkinter

class simpleapp_tk(Tkinter.Tk):
					
		def __init__(self, parent):
				Tkinter.Tk.__init__(self,parent)
				self.parent = parent
				self.initialize()
		
		def initialize(self):
				master = self.grid()
				b = Tkinter.Button(self, text= u"Hello!")
				b.grid(column = 0, row = 0)
				C = Tkinter.Canvas(master, bg = "gray", height = 600, width = 800)
				r = 300
				C.create_oval(400-r,300-r,400+r, 300 + r,fill = "blue", outline = "")	
				C.pack()			
				
if __name__ == "__main__":
		app = simpleapp_tk(None)
		app.title('Poop Emoji Here')
		app.mainloop()
