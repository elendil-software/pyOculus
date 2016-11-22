#!/bin/bash

### BEGIN INIT INFO
# Provides:          pyoculus
# Required-Start:    $local_fs $network $named $time $syslog indi 
# Required-Stop:     $local_fs $network $named $time $syslog indi
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# X-Interactive:     true
# Short-Description: AllSky program
# Description:       pyOculus service to take images continuosly
### END INIT INFO
# DONT LOADED BY rcconf ??

NAME=pyOculus

ROOTDIR="/mnt/monitorstorage"
DATADIR=$ROOTDIR"/data/oaj/allsky"

SCRIPTPATH="/home/pi/pyOculus/pyOculus"
SCRIPT="./main.py"
SENSE="./sensehat.py"	# Empty to disable.
RUNAS=pi

STATUSDIR=$ROOTDIR"/data/oaj/allsky/status"
PIDFILE=$STATUSDIR"/pyOculus.pid"
LOGFILE=$STATUSDIR"/pyOculus.txt.log"


start() {
	# Start MAIN program
	if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE); then
		echo 'pyOculus.sh: Already running' >&2
		return 1
	fi
	echo 'pyOculus.sh: Starting ...' >&2
	if [ "$(echo $USER)" = "root" ]; then
		su -c "$SCRIPT" $RUNAS &
	else
		$SCRIPTPATH/$SCRIPT &
	fi
	echo $! > "$PIDFILE"
	if [ ! -z "$SENSE" ]; then
		$SCRIPTPATH/$SENSE "beg"
	fi
	echo 'pyOculus.sh: Process started' >&2
}

stop() {
	# Stop MAIN program
	if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
		echo 'pyOculus.sh: Process not running' >&2
		return 1
	fi
	echo 'pyOculus.sh: Stopping service...' >&2
	kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
	echo 'pyOculus.sh: Process stopped' >&2
	if [ ! -z "$SENSE" ]; then
		$SCRIPTPATH/$SENSE "stp"
	fi
}

viewlog() {
	# To show logdile continuosly
	lxterminal -t "pyOculus log" --geometry=110x15 -e "watch -n 1 tail $LOGFILE" &
}

mountdir() {
	# Check recource to save data is mounted
	if [ ! "$(mount | grep $1)" ] ; then
		echo "pyOculus.sh: Mounting "$1" ..."
		sudo /bin/mount $1
		sleep 2
		return 0
	fi
}

checkdir() {
	if [ -d "$1" ]; then
		return 0
	else
		echo "pyOculus.sh: ERROR $1 not accesible!"
		exit 1
	fi
}


webimage() {
	# Convert latest PNG to JPG for webpage
	if [ -f $PIDFILE ]; then
		convert -quality 90% -resize 75% $DATADIR/tonight/latest.png $DATADIR/tonight/latest.jpg
	fi
}

make_avi15m() {
	# Next make a list of all .png files created in the last 15 minutes and make a movie out of them
	#if [ -f $PIDFILE ]; then
		# Tonight
		night=`date +%Y%m%d -d "-12 hour"`
		find $DATADIR/png/$night/20*.png -type f -cmin -15 -exec cat {} \; | /usr/local/bin/ffmpeg -f image2pipe -framerate 5 -i - -s 696x520 -vcodec libx264  -pix_fmt yuv420p $DATADIR/tonight/latest_15m.mp4 -y
	#fi
}

make_avi24h() {
	# Next make a list of all .png files created in the last 24h and make a movie out of them
	#if [ -f $PIDFILE ]; then
		# Tonight
		night=`date +%Y%m%d -d "-12 hour"`
		find $DATADIR/png/$night/*.png -type f -cmin -1440 -exec cat {} \; | /usr/local/bin/ffmpeg -f image2pipe -framerate 5 -i - -s 696x520 -vcodec libx264  -pix_fmt yuv420p $DATADIR/tonight/latest_24h.mp4 -y
	#fi
}

make_gif() {
	if [ -f $PIDFILE ]; then
		night=`date +%Y%m%d -d "-12 hour"`
		#find $DATADIR/png/$night/20*.png -type f -cmin $1 
		find $DATADIR/png/$night/*.png -type f  -cmin +1 -print0 | \
			xargs -0 -I{} find '{}' -cmin -15 \
			> /tmp/$2 && \
		nice -n 5 convert -delay 10 -loop 0 \
			@/tmp/$2 > /tmp/$3
		cp /tmp/$2 $DATADIR/tonight/$2
		cp /tmp/$3 $DATADIR/tonight/$3
	fi
}


### MAIN ###

case "$1" in
  start)
	mountdir $ROOTDIR
	checkdir $STATUSDIR
	
	export PYTHONPATH=$SCRIPTPATH:$PYTHONPATH
	cd $SCRIPTPATH
	start 
	;;
  stop)
	export PYTHONPATH=$SCRIPTPATH:$PYTHONPATH
	cd $SCRIPTPATH
	stop
	;;
  restart)
	mountdir $ROOTDIR
	checkdir $STATUSDIR
	export PYTHONPATH=$SCRIPTPATH:$PYTHONPATH
	cd $SCRIPTPATH
	stop
	start 
	;;
  onboot)
	echo "pyOculus.sh: Waiting to boot finished..."
	sleep 60
	mountdir $ROOTDIR
	checkdir $STATUSDIR
	export PYTHONPATH=$SCRIPTPATH:$PYTHONPATH
	cd $SCRIPTPATH
	start 
	;;
  viewlog)
	checkdir $STATUSDIR
	viewlog
	;;
  webimage)
	checkdir $DATADIR
	webimage
	;;
  gif15m)
	checkdir $DATADIR
	make_gif -15 latest_15m.list latest_15m.gif
	;;
  gif24h)
	checkdir $DATADIR
	make_gif -1440 latest_24h.list latest_24h.gif
	;;

  *)
    echo "Usage: $0 {start|stop|restart|viewlog|webimage|gif15m|gif24h}"
esac
