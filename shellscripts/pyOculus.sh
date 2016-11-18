#!/bin/bash

SCRIPTPATH="/home/pi/pyOculus/pyOculus"
SCRIPT="./main.py"
PIDFILE=$SCRIPTPATH"/run/pyOculus.pid"
RUNAS="pi"
DATAROOT="/mnt/monitorstorage"

function start {
 if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE); then
    echo 'pyOculus already running' >&2
    return 1
  fi
  echo 'Starting pyOculus…' >&2
  cd $SCRIPTPATH
  $SCRIPT &
  echo $! > "$PIDFILE"
  echo 'Service started' >&2
}

function stop {
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
    echo 'Process not running' >&2
    return 1
  fi
  echo 'Stopping service…' >&2
  kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
  echo 'Process stopped' >&2
}

function viewlog {
	lxterminal -t "pyOculus log" --geometry=110x15 -e "watch -n 1 tail /tmp/pyOculus.txt.log"
}

function mountdir {
	if [ ! "$(mount | grep $1)" ] ; then
		echo "Montando "$1
		sudo /bin/mount $1
	fi
}


case "$1" in
  start)
	export PYTHONPATH=$SCRIPTPATH:$PYTHONPATH
	mountdir $DATAROOT
	start 
	;;
  stop)
	stop
	;;
  viewlog)
	viewlog
	;;
  *)
    echo "Usage: $0 {start|stop|viewlog}"
esac



