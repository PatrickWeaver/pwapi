from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
# 🚸 Will need to import bot models like this:
# from blog.models import Post
# In case the datetime module is needed it is imported as 'dt'
# https://docs.python.org/3/library/datetime.html
import datetime as dt
from datetime import datetime
# https://docs.python.org/3/library/json.html
import json
# Create your views here.

def message(request):
    time = str(datetime.now())

    response = {
        "bot_message": "Hi, I am the bot, it is " + time + ". Thanks for sending a message.",
        "timestamp": time,
    }
    return JsonResponse(response, safe=False)
