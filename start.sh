#!/bin/bash

# Python buffers stdout. Without this, you won't see what you "print" in the Activity Logs
export PYTHONUNBUFFERED=true

# Start Gunicorn processes
echo Starting Gunicorn.
cd pwapi
exec gunicorn pwapi.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1
