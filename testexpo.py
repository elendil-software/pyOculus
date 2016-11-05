#!/usr/bin/python
# -*- encoding: utf-8 -*-

from time import sleep
from gc import collect
try:		
	from indiclient import IndiClient
except:
	print("INDiClient not installed")
	
exptime=2
filename="hola.fits"
i = 0
collect()
indiclient=IndiClient(exptime, filename)

while i< 1:
	i +=1
	print i
	# set indi server localhost and port 7624
	indiclient.setServer("localhost",7624)
	if (not(indiclient.connectServer())):
		 print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")

	# connect to indi server pause for 2 seconds
	sleep(2)
	# start endless loop, client works asynchron in background, loop stops after disconnect
	while indiclient.connected:
		sleep(0.3)
	collect()
		
del indiclient

