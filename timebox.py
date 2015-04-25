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
import modules.printer
import time

# MultiWii Initialization
#board = MultiWii("/dev/ttyUSB0")
#board = MultiWii("/dev/tty.usbserial-A801WZA1")

# Printer 
#printer = ThermalPrinter(serialport='/dev/ttyAMA0')

hour_time = time.time()

sizeX = 320
sizeY = 240
circleradius = 100
arcradius = 85
running = 0

tk = Tk()
tk.title("Timebox")
tk.geometry("320x240+0+0")
tk.configure(background='black')
#tk.attributes("-fullscreen", True)
canvas = Canvas(tk, width=sizeX, height=sizeY, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()


def boxAngle():
	global board, canvas, a, c, b, running

	canvas.delete(a)
	canvas.delete(c)
	canvas.delete(b)
	#board.getData(MultiWii.ATTITUDE)
	running = 1
	attitude = {'angx':0,'angy':0,'heading':0,'elapsed':0,'timestamp':0}
	arcStart = attitude['angx']+15+90
	arcEnd = attitude['angx']-15+90
	r = int(utils.limit(utils.mapping(attitude['angx'], -90, 10, 255, 0),0,255))
	g = int(utils.limit(utils.mapping(attitude['angx'], -20, 20,  200, 255),0,255))
	b = int(utils.limit(utils.mapping(attitude['angx'], -10, 90, 0, 255),0,255)) 
	#print "angle= %0.2f r= %d g= %d b= %d" % (board.attitude['angx'],r,g,b)
	#canvas.create_circle_arc(100, 120, 50, fill="black", style="arc", outline=utils.rgb_to_hex((r, g, b)), width=10, start=0, end=180)
	c = canvas.create_circle(sizeX/2, sizeY/2, circleradius, fill="black", outline=utils.rgb_to_hex((r, g, b)), width=10)
	a = canvas.create_circle_arc(sizeX/2, sizeY/2, arcradius, style="arc", outline="white", width=3, start=arcStart, end=arcEnd)
	b = canvas.create_circle(sizeX/2, sizeY/2, 30, fill="#11A7F4", outline="white", width=1)
	t = canvas.create_text(sizeX/2, sizeY/2,text="Go", fill="white", font=("Helvetica", 36))
	canvas.tag_bind(b, "<ButtonPress-1>", click)
	canvas.tag_bind(t, "<ButtonPress-1>", click)
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

def click(event):
	global b, update, running, printer
	canvas.delete(b)
	b = canvas.create_circle(sizeX/2, sizeY/2, 30, fill="red", outline="white", width=1)
	tk.update()
	#tk.after_cancel(update)
	print "imprimiendo..."
	time.sleep(2)
	cadena = "Tiempo %d\n" % (time.time() - hour_time)
	printer.print_text("\nHello Tania. Como estas?\n")
	printer.print_text(cadena)
	print "resuming %s" % (cadena)
	#update = boxAngle()
	#t = canvas.create_text(sizeX/2, sizeY/2,text="Printing...", fill="white", font=("Helvetica", 20))
    #tk.quit()


c = canvas.create_circle(sizeX/2, sizeY/2, circleradius, fill="black", outline="#DDD", width=10)
#canvas.create_circle_arc(100, 120, 50, fill="black", style="arc", outline="#DDD", width=10, start=0, end=180)
a = canvas.create_circle_arc(sizeX/2, sizeY/2, arcradius, style="arc", outline="white", width=5, start=0+15, end=0-15)
b = canvas.create_circle(sizeX/2, sizeY/2, 40, fill="red")
#canvas.tag_bind(b, "<ButtonPress-1>", click)

update = boxAngle()
tk.mainloop()  

