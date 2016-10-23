import os
import yaml

cfgfile = '%s/config.yaml' % os.getcwd()
cfgdata = yaml.load(open(cfgfile, 'r'))

OBSERVATORY = cfgdata["Observatory"]

DATA_DIR = cfgdata["Data"]["data_dir"]

INSTRU = cfgdata["Instru"]["id"]
EXP_NIGHT =  cfgdata["Expos"]["night"]
EXP_DAY =  cfgdata["Expos"]["day"]



