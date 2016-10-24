from os import makedirs
from os.path import isdir, dirname, exists
from subprocess import check_output
import re

# Check prerequisities previously to take an image.
def check_prev(test):
	itsOk = True
	reasons = []
	
	# Check DATA_DIR is accesible
	mounted = isdir(test['datadir'])
	if not mounted:
		reasons.append("%s is not accesible." % test['datadir'])
	itsOk = itsOk * mounted

	# Check device plugged
	plugged = False
	device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
	df = check_output("lsusb")
	devices = []
	for i in df.split('\n'):
		if i:
			info = device_re.match(i)
			if info:
				dinfo = info.groupdict()
				dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
				devices.append(dinfo)
	for dev in devices:
		if dev['tag'].strip() == test['usbtag']:
			plugged = True
	
	if not plugged:
		reasons.append("Camera is not plugged.")
	itsOK = itsOk * plugged
	
	# check_output fail if not exist
	try:
		pid_indiserver = check_output(["pidof","indiserver"])
		pid_indisxccd = check_output(["pidof","indi_sx_ccd"])
		process = True
		
	except:
		process = False
	
	if not process:
		reasons.append('indiserver is not running.')
	itsOk = itsOk * process

	return itsOk, reasons


# Create a dir if path's filename need it.
def check_dir(filename):
	directory = dirname(filename)
	if not exists(directory):
		makedirs(directory)
	return filename

