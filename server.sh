#!/bin/bash
BASE=`echo "$0" | sed -e "s/[^\/]*$//"`
NAME="Poppy servers"
PYTHON_CMD="local.virtualenv/bin/python"
PYTHON_SCRIPT="start_servers.py"
PID_FILE="/tmp/poppy_server.pid"


. /lib/lsb/init-functions
export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"

set -e

case "$1" in                                                                                                                                                                                                                                                                   
	start)
		log_daemon_msg "Starting ${NAME} daemon"
		start-stop-daemon --start --pidfile $PID_FILE  --chdir $BASE --chuid 1000:1000 --make-pidfile --background --startas ${PYTHON_CMD} -- ${PYTHON_SCRIPT}
	;;                                                                                                                                                                                                                                                               
	stop)
		log_daemon_msg "Stopping ${NAME} daemon"
		start-stop-daemon --stop --pidfile $PID_FILE --oknodo 
	;;
	status)
		status_of_proc -p $PID_FILE "${PYTHON_SCRIPT}" "${NAME}"
	;;
	*)
		echo "Usage: $0 {start|stop|status}"
		exit 1
esac
