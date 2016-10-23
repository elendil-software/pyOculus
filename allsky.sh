#!/bin/bash

USBdir="/media/pi/ALLSKY_USB"
CAMERAid="ID 1278:0509 Starlight Xpress"

# Check camera is plugged
CAMplugged=`lsusb | grep -e "$CAMERA"`

USBplugged=''
# Check USBdrive is plugged
if [ -d "$USBdir" ] ; then
	if [ "$(mount | grep $USBdir)" ] && [ "$(ls -A $USBdir)" ] ; then
		USBplugged='ok'
	fi
fi

# Check All is Ok.
if [ -z "$CAMplugged" ] || [ -z "$USBplugged" ]
then
        printf "Device USB or CAM is unplugged\n"
        exit
else
	datadir=$USBdir/data/oaj/allsky
	# Tonight 
	night=`date +%Y%m%d -d "-12 hour"`
	
	#source /home/pi/env/allsky/bin/activate
	python /home/pi/pyOculus/pyOculus/snapper.py
	convert -quality 90% -resize 75% $datadir/tonight/latest.png $datadir/tonight/latest.jpg
	#/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.jpg s3://www.zemogle.uk/allsky/
	#/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync images/*.json s3://www.zemogle.uk/allsky/

	# Next make a list of all .png files created in the last 15 minutes & Make a movie out of them
	find $datadir/png/$night/20*.png -type f -cmin -1440 -exec cat {} \; | /usr/local/bin/ffmpeg -f image2pipe -framerate 5 -i - -s 696x520 -vcodec libx264  -pix_fmt yuv420p /tmp/latest_15m.mp4 -y
	#/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync /home/pi/latest.mp4 s3://www.zemogle.uk/allsky/
	mv /tmp/latest_15m.mp4 $datadir/tonight/latest_15m.mp4
	#/usr/local/bin/s3cmd -c /home/pi/.s3cfg --no-progress sync /home/pi/images/*_.mp4 s3://www.zemogle.uk/allsky/archive/
fi
