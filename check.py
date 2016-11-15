from os import makedirs, statvfs
from os.path import isdir, dirname, exists
from subprocess import check_output
import re

from config import DATA_DIR, INSTR_TAG, MEMFREE, SPACEFREE


def _check_datadir(directory):
	'''
	Check DATA_DIR is accesible (mounted)
	'''
	mounted = isdir(directory)
	# Summary
	if not mounted:
		reason = "%s is not accesible." % (directory)
		return reason
	else:
		return True


def _check_usbplug(usbtag):
	'''
	Check device plugged # Thanks StackOverFlow
	'''
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
		if dev['tag'].strip() == usbtag:
			plugged = True
	# Summary
	if not plugged:
		reason = "Camera is not plugged."
		return reason
	else:
		return True


def _check_indi():
	'''
	Check indiserver and indidriver is running
	'''
	# check_output fail if not exist
	try:
		pid_indiserver = check_output(["pidof","indiserver"])
		pid_indisxccd = check_output(["pidof","indi_sx_ccd"])
		process = True
	except:
		process = False
	# Summary
	if not process:
		reason = "indiserver is not running."
		return reason
	else:
		return True
	

def check_prev():
	'''
	Check prerequisities previously to take an image.
	''' 
	reasons = ""
	tests = ( \
		_check_datadir(DATA_DIR), \
		_check_usbplug(INSTR_TAG), \
		_check_indi(), \
		)
	for test in tests:
		if not test:
			reasons += test
	if reasons == "":
		return True
	else:
		return reasons
	

def check_space():
	'''
	Check space on disk. Thanks StackOverFlow
	'''
	statv = statvfs(DATA_DIR)
	total = float(statv.f_frsize * statv.f_blocks)  # Size of filesystem in bytes
	free = float(statv.f_frsize * statv.f_bfree)   # Actual number of free bytes
	ratio = free/total
	if ratio < SPACEFREE:
		freespace = False
	else:
		freespace = True
		
	if not freespace:
		reason = "Out of space (ratio free:%.1f%%) in %s" % (ratio, DATA_DIR)
		return reason
	else:
		return True
		

def check_dir(filename):
	'''
	Create a dir if path's filename need it.
	filename: filename with absolute path included.
	'''
	try:
		directory = dirname(filename)
		if not exists(directory):
			makedirs(directory)
		return True
	except:
		reason = "Fail creating directory %s" % (directory)
		return reason


def check_memory():
	'''
	Check free memory avaiable
	leak memory on driver? it doesn't release ~3MB every iteration
	'''
	mymem = _get_memory()
	if mymem['used'] > (1-MEMFREE)*mymem['total']:
		reason = "Reaching memory limt (used: %.1f%% > %.1f%%)" % \
			(100.*mymem['used']/mymem['total'], 100.*(1-MEMFREE))
		return reason
	else:
		return True


def _get_memory():
	'''
	Get node total memory and memory usage # Thanks StackOverFlow
	'''
	with open('/proc/meminfo', 'r') as mem:
		ret = {}
		tmp = 0
		for i in mem:
			sline = i.split()
			if str(sline[0]) == 'MemTotal:':
				ret['total'] = int(sline[1])
			elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
				tmp += int(sline[1])
		ret['free'] = tmp
		ret['used'] = int(ret['total']) - int(ret['free'])
	return ret
