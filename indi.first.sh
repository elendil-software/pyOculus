#!/bin/bash
CAMERAid="ID 1278:0509 Starlight Xpress"

# Check camera is plugged
CAMplugged=`lsusb | grep -e "$CAMERAid"`

# Check All is Ok.
if [ -z "$CAMplugged" ]
then
    echo -e '\n\033[31;1mDevice USB or CAM is unplugged\033[0m\n'
    xmessage -center "Device USB or CAM is unplugged"
    exit
else
	pkill indiserver
	indiserver -m 128 -p 7624 indi_sx_ccd &
	sleep 2
	# set the connection ON
	indi_setprop -p 7624 "SX CCD SuperStar.CONNECTION.CONNECT=On" &
	sleep 2
	indi_getprop -p 7624 &
fi

