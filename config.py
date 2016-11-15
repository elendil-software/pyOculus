from os import getcwd
from yaml import load
import logging


# getting path
def _get_scriptpath():
	return getcwd()	

# reading config from yaml file
def _get_config(cfgpath):
	cfgfile = '%s/config.yaml' % cfgpath
	cfgdata = load(open(cfgfile, 'r'))
	return cfgdata

# logging config
def _set_logger(logfile, loglevel):
	if loglevel == "DEBUG":
		level = logging.DEBUG
	elif loglevel == "INFO":
		level = logging.INFO
	else:
		level = logging.WARNING

	if logfile.startswith("./"):
		logfile = "%s/%s" % (SCRIPTPATH, logfile)
	
	logging.basicConfig(\
		level=level,\
		filename="{0}.log".format(logfile),\
		format="%(asctime)s [%(levelname)-5.5s]  %(message)s"\
		)
	logger = logging.getLogger()
	logger.debug("Logger initialised.")	
	return logger


SCRIPTPATH = _get_scriptpath()
_cfgdata = _get_config(SCRIPTPATH)

MEMFREE =	_cfgdata["Basic"]["memfree"]
SPACEFREE =	_cfgdata["Basic"]["spacefree"]
SHMOD = 	_cfgdata["Basic"]["sensehat"]
DATA_DIR = 	_cfgdata["Basic"]["data_dir"]

OBSERVATORY=_cfgdata["Observatory"]

INSTR_DEV = _cfgdata["Instru"]["device"]
INSTR_TAG = _cfgdata["Instru"]["usbtag"]
INSTR_ID = 	_cfgdata["Instru"]["id"]
EXP_MAX =	_cfgdata["Instru"]["expo_max"]
EXP_MIN =  	_cfgdata["Instru"]["expo_min"]
SUNDT = 	_cfgdata["Instru"]["sundt"]

logger = _set_logger( \
	_cfgdata["Basic"]["logfile"], _cfgdata["Basic"]["loglevel"])

