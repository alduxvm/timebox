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
from modules.printer import ThermalPrinter
import time, csv, datetime, random

debug = True

# MultiWii Initialization
#board = MultiWii("/dev/ttyUSB0")
#board = MultiWii("/dev/tty.usbserial-A801WZA1")

# CSV data Initialization
# Read CSV file
reader = reader = csv.reader(open('data.csv', 'rU'), delimiter=';')
# Put the CSV info into a list
events = list(reader)
# Sort the list by date (sort of...)
events.sort()
# Delete the first error element of the list which is blank data
events.pop(0)
# Arrange events according date (substract 70 days from all dates)
for i in range(len(events)):
	try:
		csvdate = datetime.datetime.strptime(events[i][0],"%Y-%m-%dT%H:%M:%S")
	except:
		csvdate = datetime.datetime.strptime(events[i][0],"%Y-%m-%d")
	tempdate = csvdate - datetime.timedelta(days=70)
	events[i][0] = tempdate.strftime('%d %b %Y')

# Printer 
printer = ThermalPrinter(serialport='/dev/ttyAMA0')

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
	global b, update, running, printer, events, board
	canvas.delete(b)
	b = canvas.create_circle(sizeX/2, sizeY/2, 30, fill="red", outline="white", width=1)
	tk.update()
	#tk.after_cancel(update)
	print "imprimiendo..."
	#time.sleep(0.5)
	valor = random.randint(0,len(events)-1)
	#valor = utils.mapping(board.attitude)
	message = "\n%s\nOn %s\n%s\n\nMore info: %s\n\n" % (events[valor][1],events[valor][0],events[valor][2],events[valor][3])
	print message
	printer.justify("C")
	printer.inverse_on()
	printer.bold_on()
	printer.print_text("TIME BOX")
	printer.inverse_off()
	printer.print_text("\n______________\n")
	printer.bold_off()
	printer.print_text("According to:\n")
	printer.bold_on()
	printer.print_text(str(valor))
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
	printer.print_text("\n\n:)\n____________________________\n\n\n")
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

