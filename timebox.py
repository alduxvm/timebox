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

# MultiWii Initialization
#board = MultiWii("/dev/ttyUSB0")
board = MultiWii("/dev/tty.usbserial-A801WZA1")

sizeX = 320
sizeY = 240
circleradius = 100
arcradius = 85

tk = Tk()
tk.title("Timebox")
tk.geometry("320x240+0+0")
tk.configure(background='black')
#tk.attributes("-fullscreen", True)
canvas = Canvas(tk, width=sizeX, height=sizeY, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()

def boxAngle():
	global board, canvas, a, c
	canvas.delete(a)
	canvas.delete(c)
	board.getData(MultiWii.ATTITUDE)
	arcStart = board.attitude['angx']+15+90
	arcEnd = board.attitude['angx']-15+90
	r = int(utils.limit(utils.mapping(board.attitude['angx'], -90, 10, 255, 0),0,255))
	g = int(utils.limit(utils.mapping(board.attitude['angx'], -20, 20,  200, 255),0,255))
	b = int(utils.limit(utils.mapping(board.attitude['angx'], -10, 90, 0, 255),0,255)) 
	#print "angle= %0.2f r= %d g= %d b= %d" % (board.attitude['angx'],r,g,b)
	#canvas.create_circle_arc(100, 120, 50, fill="black", style="arc", outline=utils.rgb_to_hex((r, g, b)), width=10, start=0, end=180)
	c = canvas.create_circle(sizeX/2, sizeY/2, circleradius, fill="black", outline=utils.rgb_to_hex((r, g, b)), width=10)
	a = canvas.create_circle_arc(sizeX/2, sizeY/2, arcradius, style="arc", outline="white", width=3, start=arcStart, end=arcEnd)
	tk.after(100, boxAngle)

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle_arc = _create_circle_arc


c = canvas.create_circle(sizeX/2, sizeY/2, circleradius, fill="black", outline="#DDD", width=10)
#canvas.create_circle_arc(100, 120, 50, fill="black", style="arc", outline="#DDD", width=10, start=0, end=180)
a = canvas.create_circle_arc(sizeX/2, sizeY/2, arcradius, style="arc", outline="white", width=5, start=0+15, end=0-15)

boxAngle()
tk.mainloop()  

