from os import getcwd
from yaml import load
import logging

# reading config from yaml file
def get_config(cfgpath):
	cfgfile = '%s/config.yaml' % cfgpath
	cfgdata = load(open(cfgfile, 'r'))
	return cfgdata

# logging config
def set_logger(logpath, loglevel):
	if loglevel == "DEBUG":
		level = logging.DEBUG
	elif loglevel == "INFO":
		level = logging.INFO
	else:
		level = logging.WARNING
	
	logging.basicConfig(\
		level=level,\
		filename="{0}/{1}.log".format(logpath, "amen.txt"),\
		format="%(asctime)s [%(levelname)-5.5s]  %(message)s"\
		)
	logger = logging.getLogger()
	logger.info("Config loaded")
	
	'''
	
	logger = logging.getLogger()
	# File log
	fileHandler = logging.FileHandler("{0}/{1}.log".format(logpath, "amen.txt"))
	fileHandler.setFormatter(logFormatter)
	fileHandler.setLevel(logging.DEBUG)
	logger.addHandler(fileHandler)
	'''
	# Console log
	'''
	consoleHandler = logging.StreamHandler()
	#consoleHandler.setFormatter(logFormatter)
	#consoleHandler.setLevel(logging.DEBUG)
	logger.addHandler(consoleHandler)
	'''
	return logger

scriptpath = getcwd()

cfgdata = get_config(scriptpath)
MEMFREEMIN= cfgdata["Basic"]["memfree"]
SHMOD = 	cfgdata["Basic"]["sensehat"]
OBSERVATORY = cfgdata["Observatory"]
INSTR_TAG = cfgdata["Instru"]["usbtag"]
INSTR_ID = 	cfgdata["Instru"]["id"]
DATA_DIR = 	cfgdata["Instru"]["data_dir"]
EXP_NIGHT =	cfgdata["Instru"]["expo_night"]
EXP_DAY =  	cfgdata["Instru"]["expo_day"]
SUNDT = 	cfgdata["Instru"]["sundt"]

logger = set_logger(scriptpath, cfgdata["Basic"]["loglevel"])

