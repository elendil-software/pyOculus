import numpy
from astropy.io import fits
from astropy.visualization import (LogStretch)
from PIL import Image, ImageFont, ImageDraw
import json


# Creating PNG imagesipython
def make_image(parms, fitsfile, pngfile):
	'''
	Function to read in the FITS file from Oculus.
	- performe a LogStretch
	- Write image array to a PNG
	'''
	img_data = fits.getdata(fitsfile)
	img_data = img_data - numpy.min(img_data)
	img_data = img_data / numpy.max(img_data)
	stretch = LogStretch()
	img_data = stretch(img_data)
	img_data = img_data * 255
	result = Image.fromarray(img_data.astype(numpy.uint8))
	fontB = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 32)
	fontS = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 24)
	titletxt = '%s All Sky - %s' % (parms['observatory'], parms['night'])
	timetxt = 'timestamp = %s' % (parms['utc'].strftime("%Y-%m-%d %H:%M:%S"))
	if parms['exp'] >= 1:
		expotxt = 'exposure = %.0f s' % (parms['exp'])
	else:
		expotxt = 'exposure = %.4f s' % (parms['exp'])
		
	draw = ImageDraw.Draw(result)
	draw.text((10, 10), titletxt, font=fontB, fill=255)
	draw.text((10, 60), timetxt, font=fontS, fill=255)
	draw.text((10, 100), expotxt, font=fontS, fill=255)
	result.save(pngfile)
	del fontB, fontS, titletxt, timetxt, expotxt
	del img_data, result, draw
	return


# Creating JSON file
def make_json(parms, jsonfile):
	latestdata = {
	'night': parms['night'],
	'time' : parms['utc'].strftime("%a, %d %b %Y %H:%M:%S GMT+0000"),
	'expo' : parms['exp']
	}
	latestjson = json.dumps(latestdata)
	f = open(jsonfile,'w')
	f.write("%s" % latestjson)
	f.close()
	del f, latestjson, latestdata
	return
