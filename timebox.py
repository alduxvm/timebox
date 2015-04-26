#!/usr/bin/env python
""" Timebox """

__author__ = "Aldo Vargas"
__designer__ = "Tania Ortega"
__copyright__ = "Copyright 2015 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

from Tkinter import *
from modules.pyMultiwii import MultiWii	
import modules.utils as utils
from modules.printer import ThermalPrinter
import time, csv, datetime, random


# MultiWii Initialization
board = MultiWii("/dev/ttyUSB0")
#board = MultiWii("/dev/tty.usbserial-A801WYAE")	

# Events data Initialization
reader = reader = csv.reader(open('data.csv', 'rU'), delimiter=';')
events = list(reader)
events.sort()
events.pop(0)
for i in range(len(events)):
	try:
		csvdate = datetime.datetime.strptime(events[i][0],"%Y-%m-%dT%H:%M:%S")
	except:
		csvdate = datetime.datetime.strptime(events[i][0],"%Y-%m-%d")
	tempdate = csvdate - datetime.timedelta(days=70)
	events[i][0] = tempdate.strftime('%d %b %Y')

# Printer Initialization
try:
	printer = ThermalPrinter(serialport='/dev/ttyAMA0')
except:
	pass

sizeX = 320
sizeY = 240
circleradius = 100
arcwidth = 15
ringwidth = 20
arcradius = 80
running = 0

tk = Tk()
tk.title("Timebox")
tk.geometry("320x240+0+0")
tk.configure(background='black')
tk.attributes("-fullscreen", True)
canvas = Canvas(tk, width=sizeX, height=sizeY, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()


""" Main GUI update function, called each 150 miliseconds """
def boxAngle():
	global board, canvas, a, c, b, running

	canvas.delete(a)
	canvas.delete(c)
	canvas.delete(b)
	board.getData(MultiWii.ATTITUDE)
	running = 1
	#attitude = {'angx':0,'angy':0,'heading':0,'elapsed':0,'timestamp':0}
	arcStart = board.attitude['angx']+arcwidth+90
	arcEnd = board.attitude['angx']-arcwidth+90
	#r = int(utils.limit(utils.mapping(board.attitude['angx'], -90, 10, 255, 0),0,255))
	#g = int(utils.limit(utils.mapping(board.attitude['angx'], -20, 20,  200, 255),0,255))
	#b = int(utils.limit(utils.mapping(board.attitude['angx'], -10, 90, 0, 255),0,255)) 
	r = int(utils.limit(utils.mapping(board.attitude['angx'], -100, 10, 255, 0),0,255))
	g = int(utils.limit(utils.mapping(board.attitude['angx'], -20, 20,  200, 255),0,255))
	b = int(utils.limit(utils.mapping(board.attitude['angx'], -10, 100, 0, 255),0,255)) 
	#print "angle= %0.2f r= %d g= %d b= %d" % (board.attitude['angx'],r,g,b)
	#canvas.create_circle_arc(100, 120, 50, fill="black", style="arc", outline=utils.rgb_to_hex((r, g, b)), width=10, start=0, end=180)
	c = canvas.create_circle(sizeX/2, sizeY/2, circleradius, fill="black", outline=utils.rgb_to_hex((r, g, b)), width=ringwidth)
	a = canvas.create_circle_arc(sizeX/2, sizeY/2, arcradius, style="arc", outline="white", width=7, start=arcStart, end=arcEnd)
	b = canvas.create_circle(sizeX/2, sizeY/2, 30, fill="#ED1F24")
	t = canvas.create_text(sizeX/2, sizeY/2,text="GO", fill="white", font=("Helvetica", 30))
	canvas.tag_bind(b, "<ButtonPress-1>", click)
	canvas.tag_bind(t, "<ButtonPress-1>", click)
	tk.after(150, boxAngle)

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle_arc = _create_circle_arc


""" Function called everytime the Go button is pressed, this is the one that prints stuff """
def click(event):
	global b, update, running, printer, events, board
	canvas.delete(b)
	b = canvas.create_circle(sizeX/2, sizeY/2, 30, fill="red", outline="white", width=1)

	if board.attitude['angx'] == 0.0:
		valor = random.randint(0,len(events)-1)
	else:
		valor = int(utils.limit(utils.mapping(board.attitude['angx'],-110,110,0,len(events)-1),0,len(events)-1))
	print "\nStart printing... ang %0.2f, value %d" % (board.attitude['angx'],valor)
	try: 
		url = events[valor][3]
	except:
		url = "No URL... sorry"

	message = "%s\nOn %s\n%s\nMore info: %s\n" % (events[valor][1],events[valor][0],events[valor][2],url)
	print message
	try:
		printer.justify("C")
		printer.inverse_on()
		printer.bold_on()
		printer.print_text("TIME BOX")
		printer.inverse_off()
		printer.print_text("\n______________\n")
		printer.bold_off()
		printer.print_text("According to:\n")
		printer.bold_on()
		printer.print_text(str(board.attitude['angx']))
		printer.print_text(" degrees")
		printer.bold_off()
		printer.print_text("\nof inclination\n______________\n\n")
		printer.bold_on()
		printer.print_text(events[valor][1])
		printer.bold_off()
		printer.print_text("\n")
		printer.print_text(events[valor][0])
		printer.print_text("\n\n")
		printer.print_text(events[valor][2])
		printer.print_text("\n\nMore info:\n")
		printer.print_text(events[valor][3])
		printer.print_text("\n\n:)\n____________________________\n\n\n\n")
	except:
		print "Error while printing, perhaps no printer attached."

""" Function to exit app, press top left corner to exit """
def exitApp(event):
	print "\nBye!!\n\n\n"
	tk.quit()

c = canvas.create_circle(sizeX/2, sizeY/2, circleradius, fill="black", outline="#DDD", width=ringwidth)
#canvas.create_circle_arc(100, 120, 50, fill="black", style="arc", outline="#DDD", width=10, start=0, end=180)
a = canvas.create_circle_arc(sizeX/2, sizeY/2, arcradius, style="arc", outline="white", width=7, start=0+arcwidth, end=0-arcwidth)
b = canvas.create_circle(sizeX/2, sizeY/2, 40, fill="red")

exit = canvas.create_circle(0, 0, 50, fill="black")
canvas.tag_bind(exit, "<ButtonPress-1>", exitApp)

update = boxAngle()
tk.mainloop()  

