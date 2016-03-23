#!/bin/bash

NAME="Brick"                                            # Name of the application
DJANGODIR=/home/deploy/Pinbot
SOCKFILE=/data/brick/tmp/gunicorn.sock     # we will communicte using this unix socket
USER=deploy                                                   # the user to run as
GROUP=deploy                                                  # the group to run as
NUM_WORKERS=2                                               # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=Brick.settings                   # which settings file should Django use, change to
# myproject.settings.prod if necessary
DJANGO_WSGI_MODULE=Brick.wsgi                           # WSGI module name
LOG_FILE='/data/brick/log/gunicorn/brick_access.log'
ERROR_LOG_FILE='/data/brick/log/gunicorn/brick_err.log'

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source pin_venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --log-level=info \
    --bind=unix:$SOCKFILE \
    --access-logfile=$LOG_FILE \
    --error-logfile=$ERROR_LOG_FILE
