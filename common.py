from datetime import datetime, timedelta
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
from astroplan import Observer

# My libs
from config import OBSERVATORY, SUNDT
from config import logger


class Night():
	'''
	To calculate and remember night period
	'''
	def __init__(self, observatory, currenttime):
		sunrise, sunset = self.get_riseset(observatory, currenttime)
		self.night8 = self.get_night(currenttime)
		self.observatory = observatory.name
		self.sunrise = sunrise
		self.sunset = sunset
		self.obsstart = sunset - timedelta(minutes = SUNDT)
		self.obsend = sunrise + timedelta(minutes = SUNDT)
		
	def __str__( self ):
		txt = "Night of %s at %s\n" % (self.night8, self.observatory)
		txt += "Sunset: %s        Sunrise: %s\n" % (self.sunset, self.sunrise)
		txt += "ObsStart: %s      ObsEnd: %s" % (self.obsstart, self.obsend)
		return txt
		
	# Sunset, Sunrise
	def get_riseset(self, observatory, currenttime):
		logger.debug("Calculating sunrise/sunset.")
		time = Time(currenttime)
		if currenttime.hour < 12:
			sunset_tonight = observatory.sun_set_time(time, which='previous')
			sunrise_tonight = observatory.sun_rise_time(time, which='nearest')
		else:
			sunset_tonight = observatory.sun_set_time(time, which='nearest')
			sunrise_tonight = observatory.sun_rise_time(time, which='next')
			
		return (sunrise_tonight.datetime, sunset_tonight.datetime)

	# Which night? Change on every midday
	def get_night(self, currenttime):
		logger.debug("Getting night8 string.")
		currenthour = float(currenttime.strftime('%H'))+float(currenttime.strftime('%M'))/60.
		if currenthour > 12:
			night8 = currenttime.strftime('%Y%m%d')
		else:
			night8 = (currenttime - timedelta(1)).strftime('%Y%m%d')
		del currenttime
		return night8
	
def set_location():
	'''
	Establishing observatory location with astroplan.Observer
	'''
	logger.debug("Establishing observatory location")
	lat = OBSERVATORY["lati"]
	lon = OBSERVATORY["long"]
	elev = OBSERVATORY["elev"]
	name = OBSERVATORY["name"]
	timezone = "UTC"       	# Same computer clock works!
	logoffset = 0			# To do test in daylight.
	location = EarthLocation.from_geodetic((lon*u.deg+logoffset*u.deg), lat*u.deg, elev*u.m)
	observatory = Observer(location=location, name=name, timezone=timezone)
	return observatory
