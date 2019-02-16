#!/bin/bash

if ["$ENV" = "GLITCH" ]
then
    echo "GLITCH"
else
    echo ""
fi

pip3 install gunicorn --user

pip3 install -r requirements.txt --user

# Python buffers stdout. Without this, you won't see what you "print" in the Activity Logs
export PYTHONUNBUFFERED=true

cd pwapi
python3 manage.py runserver


# Start Gunicorn processes
#echo Starting Gunicorn.
#cd pwapi
#exec gunicorn pwapi.wsgi:application \
#    --bind 0.0.0.0:8000 \
#    --workers 3
