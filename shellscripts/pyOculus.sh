#!/bin/bash

SCRIPTPATH="/home/pi/pyOculus/pyOculus"
SCRIPT="./main.py"
PIDFILE=$SCRIPTPATH"/run/pyOculus.pid"
RUNAS="pi"

ROOTDIR="/mnt/monitorstorage"
DATADIR=$ROOTDIR"/data/oaj/allsky"
LOGFILE="/tmp/pyOculus.txt.log"


function mountdir {
	# Check recource to save data is mounted
	if [ ! "$(mount | grep $1)" ] ; then
		echo "Montando "$1
		sudo /bin/mount $1
	fi
}

function start {
	# Start MAIN program
	if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE); then
		echo 'pyOculus already running' >&2
		return 1
	fi
	echo 'Starting pyOculus…' >&2
	cd $SCRIPTPATH
	$SCRIPT &
	echo $! > "$PIDFILE"
	echo 'Process started' >&2
}

function stop {
	# Stop MAIN program
	if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
		echo 'Process not running' >&2
		return 1
	fi
	echo 'Stopping service…' >&2
	kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
	echo 'Process stopped' >&2
}

function viewlog {
	# To show logdile continuosly
	lxterminal -t "pyOculus log" --geometry=110x15 -e "watch -n 1 tail $LOGFILE"
}

function webimage {
	# Convert latest PNG to JPG for webpage
	convert -quality 90% -resize 75% $DATADIR/tonight/latest.png $DATADIR/tonight/latest.jpg
}

function makevideo {
	# Next make a list of all .png files created in the last 15 minutes and make a movie out of them
	#if [ -f $PIDFILE ]; then
		# Tonight
		night=`date +%Y%m%d -d "-12 hour"`
		find $DATADIR/png/$night/20*.png -type f -cmin -15 -exec cat {} \; | /usr/local/bin/ffmpeg -f image2pipe -framerate 5 -i - -s 696x520 -vcodec libx264  -pix_fmt yuv420p $DATADIR/tonight/latest_15m.mp4 -y
	#fi
}

function video24h {
	# Next make a list of all .png files created in the last 24h and make a movie out of them
	#if [ -f $PIDFILE ]; then
		# Tonight
		night=`date +%Y%m%d -d "-12 hour"`
		find $DATADIR/png/$night/20*.png -type f -cmin -1440 -exec cat {} \; | /usr/local/bin/ffmpeg -f image2pipe -framerate 5 -i - -s 696x520 -vcodec libx264  -pix_fmt yuv420p $DATADIR/tonight/latest_24h.mp4 -y
	#fi
}



case "$1" in
  start)
	export PYTHONPATH=$SCRIPTPATH:$PYTHONPATH
	mountdir $ROOTDIR
	start 
	;;
  stop)
	stop
	;;
  viewlog)
	viewlog
	;;
  webimage)
	webimage
	;;
  makevideo)
	makevideo
	;;
  video24h)
	video24h
	;;
  *)
    echo "Usage: $0 {start|stop|viewlog|webimage|makevideo|video24}"
esac



