#!/usr/bin/python
# -*- encoding: utf-8 -*-

## exposure method 

## it's necesary separare take_exposure because exists a leak memory
## every exposure the memory used grow 3MB.
## If we take an exposure with diferent process, the memory sets free.

# my loggging
from config import logger

try:		
	from indiclient import IndiClient
except:
	txt = "INDiClient not installed"
	print txt
	logger.critical(txt)

from time import sleep
from sys import argv

# Take image through INDI
def take_exposure(exptime, filename):
	logger.debug("Taking exposure of %s seg in %s" % (exptime, filename))
	# instantiate the client
	indiclient=IndiClient(float(exptime), str(filename))
	# set indi server localhost and port 7624
	indiclient.setServer("localhost",7624)
	# connect to indi server pause for 2 seconds
	if (not(indiclient.connectServer())):
		 txt = "No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run"
		 logger.critical(txt)
		 return False
	sleep(1)
	# start endless loop, client works asynchron in background, loop stops after disconnect
	while indiclient.connected:
		sleep(0.1)
	indiclient.disconnectServer()
	del indiclient
	return True


# MAIN ###################################
if __name__ == '__main__':

	if len(argv) > 1:
		try:
			assert isinstance(float(argv[1]), float)
			assert isinstance(argv[2], str)
			resp = take_exposure(argv[1], argv[2])
		except:
			txt = "Wrong arguments? $ exposure.py texp filename"
			logger.critical(txt)
	else:
		take_exposure(1,"test_exposure.fits")
