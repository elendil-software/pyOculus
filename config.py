import os
import yaml

cfgfile = '%s/config.yaml' % os.getcwd()
cfgdata = yaml.load(open(cfgfile, 'r'))

OBSERVATORY = cfgdata["Observatory"]
INSTRU = cfgdata["Instru"]["id"]

#FILENAME_FITS = cfgdata["Data"]["namefits"]
#FILENAME_PNG = cfgdata["Data"]["namepng"]

DATA_DIR = cfgdata["Data"]["datadir"]
#FITS_DIR = cfgdata["Data"]["fitsdir"]
#PNG_DIR = cfgdata["Data"]["pngdir"]

NIGHT_EXP =  cfgdata["Expos"]["night"]
DAY_EXP =  cfgdata["Expos"]["day"]
