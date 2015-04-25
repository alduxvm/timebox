#!/usr/bin/env python

""" Timebox """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

from Tkinter import *
from modules.pyMultiwii import MultiWii	
import modules.utils as utils


class Timebox(Frame):  
    """ Implements a timebox frame widget. """                                                                
    def __init__(self, parent=None, **kw):      
        Frame.__init__(self, parent, kw)
        self.title("Timebox")
		self.geometry("320x240+0+0")
		self.configure(background='black')
		self.attributes("-fullscreen", True)
        self._sizeX = 320
		self._sizeY = 240
		self._circleradius = 100
		self._arcradius = 85  
		self.canvas = Canvas(self, width=sizeX, height=sizeY, borderwidth=0, highlightthickness=0, bg="black")
		self.canvas.grid()           

	def _create_circle(self, x, y, r, **kwargs):
    	return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
	Canvas.create_circle = _create_circle

	def _create_circle_arc(self, x, y, r, **kwargs):
	    if "start" in kwargs and "end" in kwargs:
	        kwargs["extent"] = kwargs["end"] - kwargs["start"]
	        del kwargs["end"]
	    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
	Canvas.create_circle_arc = _create_circle_arc

	def _update(self):
		#global board, canvas, a, c, b
		canvas.delete(a)
		canvas.delete(c)
		canvas.delete(b)
		#board.getData(MultiWii.ATTITUDE)
		board.attitude = {'angx':0,'angy':0,'heading':0,'elapsed':0,'timestamp':0}
		arcStart = board.attitude['angx']+15+90
		arcEnd = board.attitude['angx']-15+90
		r = int(utils.limit(utils.mapping(board.attitude['angx'], -90, 10, 255, 0),0,255))
		g = int(utils.limit(utils.mapping(board.attitude['angx'], -20, 20,  200, 255),0,255))
		b = int(utils.limit(utils.mapping(board.attitude['angx'], -10, 90, 0, 255),0,255)) 
		#print "angle= %0.2f r= %d g= %d b= %d" % (board.attitude['angx'],r,g,b)
		#canvas.create_circle_arc(100, 120, 50, fill="black", style="arc", outline=utils.rgb_to_hex((r, g, b)), width=10, start=0, end=180)
		c = canvas.create_circle(sizeX/2, sizeY/2, circleradius, fill="black", outline=utils.rgb_to_hex((r, g, b)), width=10)
		a = canvas.create_circle_arc(sizeX/2, sizeY/2, arcradius, style="arc", outline="white", width=3, start=arcStart, end=arcEnd)
		b = canvas.create_circle(sizeX/2, sizeY/2, 30, fill="#11A7F4", outline="white", width=1)
		t = canvas.create_text(sizeX/2, sizeY/2,text="Go", fill="white", font=("Helvetica", 36))
		canvas.tag_bind(b, "<ButtonPress-1>", click)
		canvas.tag_bind(t, "<ButtonPress-1>", click)
		tk.after(100, boxAngle)                     
	    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)


def main():
    root = Tk()
    tb = Timebox(root)
    #sw.pack(side=TOP)
    
    Button(root, text='Start', command=sw.Start).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop).pack(side=LEFT)
    Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=LEFT)
    
    root.mainloop()

if __name__ == '__main__':
    main()