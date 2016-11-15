import numpy
from astropy.io import fits
from PIL import Image, ImageFont, ImageDraw
import json


# Creating PNG imagesipython
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
	del data, scaled, new_scaled, max_val
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
	f = open(jsonfile,'wb')
	f.write(latestjson)
	f.close()
	del f, latestjson, latestdata
	return
