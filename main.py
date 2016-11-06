#!/usr/bin/python
# -*- encoding: utf-8 -*-

## pyOculus version Miguel Chioare / mchioare ¿at? cefca.es
## source from: https://github.com/arritrancos/pyOculus

## Many thanks to zemogle to develop first version: https://github.com/zemogle/pyOculus

try:		
	from indiclient import IndiClient
except:
	print("INDiClient not installed")

import sys
from time import sleep
from datetime import datetime, timedelta
from shutil import copyfile

# My libs
from config import logger
from config import OBSERVATORY, INSTR_ID, INSTR_TAG, DATA_DIR, EXP_DAY, EXP_NIGHT, SUNDT, SHMOD, MEMFREEMIN
import outputs
import check
from common import set_location, get_riseset, get_night, get_memory
	
# Take image through INDI
def take_exposure(exptime, filename):
	# instantiate the client
	indiclient=IndiClient(exptime, filename)
	# set indi server localhost and port 7624
	indiclient.setServer("localhost",7624)
	# connect to indi server pause for 2 seconds
	if (not(indiclient.connectServer())):
		 print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
		 return False
	sleep(1)
	# start endless loop, client works asynchron in background, loop stops after disconnect
	while indiclient.connected:
		sleep(0.3)
	indiclient.disconnectServer()
	del indiclient
	return True


# Setting time exposure
def set_exposure(observatory, currenttime):
	sunrise, sunset = get_riseset(observatory, currenttime)
	#print(sunrise, sunset, currenttime)
	if observatory.is_night(currenttime):
		if abs(sunrise - currenttime ) < timedelta(seconds=600) or abs(currenttime -sunset) < timedelta(seconds=600):
			exp = EXP_DAY
			info = "too bright yet."
		elif abs(sunrise - currenttime) < timedelta(seconds=1800) or abs(currenttime -sunset) < timedelta(seconds=1800):
			exp = EXP_NIGHT/10.
			info = "no enough dark yet"
		elif abs(sunrise - currenttime) < timedelta(seconds=5400) or (abs(currenttime -sunset) < timedelta(seconds=5400)):
			exp = EXP_NIGHT/2.
			info = "bit dark!"
		else:
			exp = EXP_NIGHT
			info = "dark expo"
	else:
		exp = EXP_DAY
		info = "sun is up!"
	logger.info("Setting exposure time to %s (%s)" % (exp, info))
	del sunrise, sunset, observatory, currenttime
	return exp


def main_images(observatory, night8):
	# Preparing exposure	
	now = datetime.utcnow()
	exp = set_exposure(observatory, now)
	datestamp = now.strftime("%Y%m%dT%H%M%S")
	# Taking a image
	fitsfile = check.check_dir('%s/raw/%s/%s-%s.fits' % (DATA_DIR, night8, INSTR_ID, datestamp))
	resp = take_exposure(exptime=exp, filename=fitsfile)
	# Creating other products from new fits
	if resp:
		parms = {
		'observatory': observatory.name,
		'night': night8,
		'exp': exp,
		'utc': now
		}
		# Make PNG files
		pngfile = check.check_dir('%s/png/%s/%s.png' % (DATA_DIR, night8, datestamp))
		latestpng = check.check_dir('%s/tonight/latest.png' % (DATA_DIR))
		outputs.make_image(parms=parms, fitsfile=fitsfile, pngfile=pngfile)
		copyfile(pngfile, latestpng)
		# Make Jasonfile
		jsonfile = check.check_dir('%s/tonight/latest.json' % (DATA_DIR))
		outputs.make_json(parms, jsonfile)
		logger.info("Saved %s - %s" % (pngfile, datetime.utcnow().isoformat()))
	else:
		logger.critical("Error!")
	

# MAIN ###################################
if __name__ == '__main__':
	
	observatory = set_location()
	currenttime = datetime.utcnow()
	night8 = get_night(currenttime)
	
	try:
		if sys.argv[1] == "loop":
			logger.debug("Entering loop on MAIN")
			mymem = get_memory()
			i = 1
			# leak memory on driver? it doesn't release ~3MB every iteration
			while mymem['used'] < MEMFREEMIN*mymem['total']:
				logger.debug("taking a loop of images (%s) until %.1f%% < %.0f%% ." % \
					(str(i).zfill(3), 100.*mymem['used']/mymem['total'], 100*MEMFREEMIN))
				main_images(observatory, night8)
				mymem = get_memory()
				i +=1
		
	except:
		print("taking one image...")
		main_images(observatory, night8)

