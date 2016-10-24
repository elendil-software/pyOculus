import os
import yaml

cfgfile = '%s/config.yaml' % os.getcwd()
cfgdata = yaml.load(open(cfgfile, 'r'))

OBSERVATORY = cfgdata["Observatory"]

INSTR_TAG = cfgdata["Instru"]["usbtag"]
INSTR_ID = 	cfgdata["Instru"]["id"]
DATA_DIR = 	cfgdata["Instru"]["data_dir"]
EXP_NIGHT =	cfgdata["Instru"]["expo_night"]
EXP_DAY =  	cfgdata["Instru"]["expo_day"]
SUNDT = 	cfgdata["Instru"]["sundt"]



