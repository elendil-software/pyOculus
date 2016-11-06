#!/usr/bin/python
# -*- encoding: utf-8 -*-

from datetime import timedelta, datetime
from time import sleep
import subprocess as sub
from os import getcwd

# My libs
from config import SUNDT, DATA_DIR, INSTR_TAG, SHMOD, logger
from check import check_prev
from common import set_location, get_riseset, shscreen

test = {
	'usbtag': INSTR_TAG,
	'datadir': DATA_DIR
}

scriptpath = getcwd()

observatory = set_location()
currenttime = datetime.utcnow()
sunrise, sunset = get_riseset(observatory, currenttime)

itsOk = True
i = 0
while itsOk == True:
	logger.debug("Daemon loop (iterarion number %s)" % i)
	i += 1
	if i > 25:
		itsOk = False
	shpos=shscreen("ini")
	# Check prerequisities
	itsOk, reasons = check_prev(test)
	if not itsOk:
		logger.critical("ERROR: %s" % " ".join(reasons))
		break
	
	if currenttime < (sunset - timedelta(minutes = SUNDT)):
		wait = (sunset - timedelta(minutes = SUNDT) - currenttime).seconds
		logger.info("Too early. Waiting %.0f minutes" % wait/60.)
		shscreen("day")
		sleep(wait)
		pass
		
	# Check currenttime in range to observe
	if currenttime >= (sunset - timedelta(minutes = SUNDT)) or \
	currenttime <= (sunrise + timedelta(minutes = SUNDT)):
		logger.info("Inside time observation period :^)")
		shpos=shscreen("exp")
		command = "%s/main.py" % scriptpath
		p = sub.Popen([command, 'loop'],stdout=sub.PIPE,stderr=sub.PIPE)
		output, errors = p.communicate()
		print output, errors
		shpos=shscreen("dld")
		#TODO: grabar un fichero status.
		pass
			
	else:
		logger.info("Observation finished!")
		itsOk = False
				
