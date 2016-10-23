#!/usr/bin/python
# -*- encoding: utf-8 -*-

try:		
	from indiclient import IndiClient
except:
	print("INDiClient not installed")
import sys, os
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
from astropy.io import fits
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
import numpy
from shutil import copyfile
import time
import json
from astroplan import Observer, download_IERS_A
from config import OBSERVATORY, INSTRU, DATA_DIR, EXP_DAY, EXP_NIGHT

# TODO: ponerle que si tiene internet, que baje actualizacion
# Tambien que compruebe si es antigua
#download_IERS_A()

resp = None

# Create a dir if path's filename need it.
def checkdir(filename):
	directory = os.path.dirname(filename)
	if not os.path.exists(directory):
		os.makedirs(directory)
	return filename


def take_exposure(exptime, filename):
	# instantiate the client
	indiclient=IndiClient(exptime, filename)
	# set indi server localhost and port 7624
	indiclient.setServer("localhost",7624)
	# connect to indi server pause for 2 seconds
	if (not(indiclient.connectServer())):
		 print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
		 return False
	time.sleep(1)

	# start endless loop, client works asynchron in background, loop stops after disconnect
	while indiclient.connected:
		time.sleep(1)
	return True


def set_exposure(observatory, currenttime):
	sunrise, sunset = rise_set(observatory, currenttime)
	exp = EXP_NIGHT
	print(sunrise, sunset, currenttime)
	if abs(sunrise - currenttime ) < timedelta(seconds=600) or abs(currenttime -sunset) < timedelta(seconds=600):
		exp = EXP_DAY
	elif abs(sunrise - currenttime) < timedelta(seconds=1800) or abs(currenttime -sunset) < timedelta(seconds=1800):
		exp = EXP_NIGHT/10.
	elif abs(sunrise - currenttime) < timedelta(seconds=5400) or (abs(currenttime -sunset) < timedelta(seconds=5400)):
		exp = EXP_NIGHT/2.
	print("Setting exposure time to %s (%s)" % (exp, sunrise-sunset))
	return exp


def set_location():
	lat = OBSERVATORY["lati"]
	lon = OBSERVATORY["long"]
	elev = OBSERVATORY["elev"]
	name = OBSERVATORY["name"]
	timezone = OBSERVATORY["tizo"]
	location = EarthLocation.from_geodetic(lat*u.deg, lon*u.deg, elev*u.m)
	observatory = Observer(location=location, name=name, timezone=timezone)
	return observatory


def rise_set(observatory, currenttime):
	time = Time(currenttime)
	sunset_tonight = observatory.sun_set_time(time, which='nearest')
	sunrise_tonight = observatory.sun_rise_time(time, which='nearest')
	return (sunrise_tonight.datetime, sunset_tonight.datetime)


def make_image(parms, fitsfile, pngfile):
	'''
	Function to read in the FITS file from Oculus.
	- find the 99.5% value
	- Make all values above 99.5% value white
	- Write image array to a PNG
	'''
	data = fits.getdata(fitsfile)
	#data1 = data.reshape(data.shape[0]*data.shape[1])
	max_val = numpy.percentile(data,99.5)
	scaled = data*256./max_val
	new_scaled = numpy.ma.masked_greater(scaled, 255.)
	new_scaled.fill_value=255.
	img_data = new_scaled.filled()
	result = Image.fromarray(img_data.astype(numpy.uint8))
	fontB = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 32)
	fontS = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 24)
	titletxt = '%s All Sky - %s' % (OBSERVATORY["name"], parms['night'])
	timetxt = 'timestamp = %s' % (parms['utc'].strftime("%Y-%m-%d %H:%M"))
	if parms['exp'] >= 1:
		expotxt = 'exposure = %.0f s' % (parms['exp'])
	else:
		expotxt = 'exposure = %.4f s' % (parms['exp'])
		
	draw = ImageDraw.Draw(result)
	draw.text((10, 10), titletxt, font=fontB, fill=255)
	draw.text((10, 60), timetxt, font=fontS, fill=255)
	draw.text((10, 100), expotxt, font=fontS, fill=255)
	result.save(pngfile)
	return


def make_json(now=datetime.now()):
	nowtimestamp = datetime.strftime(now,"%a, %d %b %Y %H:%M:%S GMT+0000")
	latestdata = {'time' : nowtimestamp}
	latestjson = json.dumps(latestdata)
	filename = '%slatest.json' % (DATA_DIR)
	f = open(filename,'wb')
	f.write(latestjson)
	f.close()
	return


if __name__ == '__main__':
	
	# Establishing exposure time
	observatory = set_location()
	currenttime = datetime.utcnow()
	exp = set_exposure(observatory, currenttime)
	# Which night?
	currenthour = float(currenttime.strftime('%H'))+float(currenttime.strftime('%M'))/60.
	if currenthour > 12:
		night8 = currenttime.strftime('%Y%m%d')
	else:
		night8 = (currenttime - timedelta(1)).strftime('%Y%m%d')
	# First, establishing filenames (reseting "now")
	now = datetime.utcnow()
	datestamp = now.strftime("%Y%m%dT%H%M")
	fitsfile = checkdir('%s/raw/%s/%s-%s.fits' % (DATA_DIR, night8, INSTRU, datestamp))
	pngfile = checkdir('%s/png/%s/%s.png' % (DATA_DIR, night8, datestamp))
	latestpng = checkdir('%s/tonight/latest.png' % (DATA_DIR))
	# Taking a image
	resp = take_exposure(exptime=exp, filename=fitsfile)
	# Creating other products from new fits
	if resp:
		parms = {
		'night': night8,
		'exp': exp,
		'utc': now
		}
		make_image(parms=parms, fitsfile=fitsfile, pngfile=pngfile)
		copyfile(pngfile, latestpng)
		#make_json(now)
		print("Saved %s - %s" % (pngfile, datetime.utcnow().isoformat()))
	else:
		print("Error!")
	
	sys.exit()
