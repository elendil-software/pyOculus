#!/usr/bin/python
'''	
To use SenseHat modul if you like (enable on config.yaml)
'''	
import sys
from random import randint

from config import SHMOD, SHORI

from sense_hat import SenseHat
sensehat = SenseHat()
sensehat.low_light = True
sensehat.set_rotation(SHORI)

def shvalue(value):
	if value == "ini":
		sensehat.clear()
		sensehat.show_letter("i",text_colour=(255,255,255)) # White
	elif value == "beg":
		sensehat.show_message("starting...", text_colour=(255,0,255)) # Pink
	elif value == "day":
		sensehat.show_letter("d",text_colour=(255,255,0)) # Yellow
	elif value == "exp":
		sensehat.set_pixel(randint(0,7),randint(0,7),(255,0,0)) # Red
	elif value == "err":
		sensehat.show_letter("E",text_colour=(255,0,0)) # Red
	elif value == "fin":
		sensehat.show_letter("F",text_colour=(0,0,255)) # Blue
	elif value == "stp":
		sensehat.show_message("stopped!.", text_colour=(255,0,255))  # Pink
	elif value == "clr":
		sensehat.clear()
	elif value == "tst":
		sensehat.show_message("test", text_colour=(0,255,255))  # Orange

# MAIN ###################################
if __name__ == '__main__':

	if len(sys.argv) == 2:
		shvalue(sys.argv[1])
	else:
		shvalue("tst")
		
