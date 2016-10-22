import os
import yaml

cfgfile = '%s/config.yaml' % os.getcwd()
cfgdata = yaml.load(open(cfgfile, 'r'))

OBSERVATORY = cfgdata["Observatory"]

FILENAME_FITS = cfgdata["Data"]["namefits"]
FILENAME_PNG = cfgdata["Data"]["namepng"]
DATA_DIR = cfgdata["Data"]["dir"]

NIGHT_EXP =  cfgdata["expos"]["night"]
DAY_EXP =  cfgdata["expos"]["day"]
