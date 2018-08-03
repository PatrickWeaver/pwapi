#!/bin/bash

# Python buffers stdout. Without this, you won't see what you "print" in the Activity Logs
export PYTHONUNBUFFERED=true

if [ "$ENV" = "GLITCH" ]
then

  # Install Python 3 virtual env
  VIRTUALENV=.data/venv

  if [ ! -d $VIRTUALENV ]; then
    python3 -m venv $VIRTUALENV
  fi

  if [ ! -f $VIRTUALENV/bin/pip ]; then
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | $VIRTUALENV/bin/python
  fi

  export PATH=$VIRTUALENV/bin:$PATH

  # Install the requirements
  pip install -r requirements.txt

  python3 pwapi/manage.py migrate
  # Run a glorious Python 3 server
  python3 pwapi/manage.py runserver 0.0.0.0:8000


else

# Start Gunicorn processes
echo Starting Gunicorn.
cd pwapi
exec gunicorn pwapi.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
fi
