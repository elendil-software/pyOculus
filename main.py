#!/usr/bin/python
# -*- encoding: utf-8 -*-

## pyOculus version Miguel Chioare / mchioare ¿at? cefca.es
## source from: https://github.com/arritrancos/pyOculus

## Many thanks to zemogle to develop first version: https://github.com/zemogle/pyOculus

import subprocess as sub
from time import sleep
from datetime import datetime, timedelta
from shutil import copyfile

# My libs
from config import SCRIPTPATH, DATA_DIR, INSTR_ID, SHMOD, EXP_MAX, EXP_MIN
from config import logger
from common import Night, set_location
from check import check_prev, check_dir, check_space, check_memory
import outputs

'''
To use SenseHat Module to show progress
'''
if SHMOD == True:
	from common import shvalue
	shvalue("ini")


def _set_exposure(when, tonight):
	'''
	Setting time exposure
		when: datetime to evaluate
		tonight: Night object with properties to comare with now
		return texp: time exposure in seconds
	'''
	if when > tonight.sunset:
		if abs(tonight.sunrise - when ) < timedelta(seconds=600) or \
		abs(when - tonight.sunset) < timedelta(seconds=600):
			texp = EXP_MIN
			info = "too bright yet."
		elif abs(tonight.sunrise - when) < timedelta(seconds=1800) or \
		abs(when - tonight.sunset) < timedelta(seconds=1800):
			texp = EXP_MAX/10.
			info = "no enough dark yet"
		elif abs(tonight.sunrise - when) < timedelta(seconds=5400) or \
		abs(now - tonight.sunset) < timedelta(seconds=5400):
			texp = EXP_MAX/2.
			info = "bit dark"
		else:
			texp = EXP_MAX
			info = "dark expo"
	else:
		texp = EXP_MIN
		info = "sun is up!"
	logger.info("Setting exposure time to %s (%s)" % (texp, info))
	return texp


def _take_fits(texp, fitsfile):
	'''
	Take fits using exposure.py calling system with subprocess
		texp: time exposure in seconds
		fitsfile: filename with absolutepath to save image
		return True it completes Ok.
	'''
	try:
		script = "%s/exposure.py" % (SCRIPTPATH)
		command = [script, str(texp), str(fitsfile)]
		logger.debug(" ".join(command))
		p = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
		output, errors = p.communicate()
		#print output, errors
		return True
	except:
		return False


def _take_images(tonight):
	'''
	Take an image and make diferents outputs: fits, png, json.
		tonight: Night class with properties to complete images.
		return True it completes Ok
	'''
	# Preparing exposure
	now = datetime.utcnow()
	texp = _set_exposure(now, tonight)
	datestamp = now.strftime("%Y%m%dT%H%M%S")
	# Check path
	fitsfile = '%s/raw/%s/%s-%s.fits' % (DATA_DIR, tonight.night8, INSTR_ID, datestamp)
	check = check_dir(fitsfile)
	if not check == True: logger.critical(check)
	# Taking a image
	resp = _take_fits(texp, fitsfile)
	# Creating other products from new fits
	if resp:
		parms = {
		'observatory': tonight.observatory,
		'night': tonight.night8,
		'exp': texp,
		'utc': now
		}
		# Make PNG files
		pngfile = '%s/png/%s/%s.png' % (DATA_DIR, tonight.night8, datestamp)
		check = check_dir(pngfile)
		if not check == True: logger.critical(check)
		latestpng = '%s/tonight/latest.png' % (DATA_DIR)
		check = check_dir(latestpng)
		if not check == True: logger.critical(check)
		outputs.make_image(parms=parms, fitsfile=fitsfile, pngfile=pngfile)
		logger.info("Saved %s" % (pngfile))
		copyfile(pngfile, latestpng)
		# Make Jasonfile
		jsonfile = '%s/tonight/latest.json' % (DATA_DIR)
		check = check_dir(jsonfile)
		if not check == True: logger.critical(check)
		outputs.make_json(parms, jsonfile)
		return True
	else:
		logger.critical("Error when take fits image!")
		sleep(10)	# To ease ctrl+c
		return False
	

def do_obs_loop(tonight):
	j = 0
	obsloop = True
	while True or j < 9999:
		j += 1
		# Check enough space on disk (DATA_DIR, SPACEMIN)
		# Check enough memory (MEMFREEMIN)
		if not check_space() or not check_memory():
			obsloop = False
			shvalue("err")
			break
		# Check currenttime in range to observe
		now = datetime.utcnow()
		if now < (tonight.obsstart) or now > (tonight.obsend):
			reason = "Out of period of observation. Exiting of loop"
			logger.info(reason)
			sleep(1)
			obsloop = False
			break
		else:
			if SHMOD == True:
				shvalue("exp")
			info = "Taking image %i... " % (j)
			if j % 10 == 0 or j == 1: 
				info += "(time end obs: %.1f hours)" % ((tonight.obsend - now).seconds/3600.)
			logger.info(info)
			_take_images(tonight)
			if SHMOD == True:
				shvalue("")
			sleep(0.1)
	
	return obsloop


# MAIN ###################################
if __name__ == '__main__':
	
	if SHMOD == True: shvalue("ini")
	logger.info(">>>>>>>> Begining" )
	# Establishing and Calculating  
	observatory = set_location()
	now = datetime.utcnow()
	tonight = Night(observatory, now)
	logger.info("start:%s, end:%s" % (tonight.obsstart, tonight.obsend) )
	
	i = 0
	while True or i < 9999:
		i += 1
		# Check prerequisities
		if not check_prev():
			shvalue("err")
			break
		# Check currenttime in range to observe
		now = datetime.utcnow()
		if now < tonight.obsstart:
			wait = (tonigh.obsstart - now).seconds
			logger.warning("Too early. Waiting %.0f minutes" % wait/60.)
			if SHMOD == True: shvalue("day")
			sleep(wait)
			pass
		
		else:
			# do images in a loop
			if not do_obs_loop(tonight):
				break
				
	if SHMOD == True: shvalue("fin")
	# Fin
