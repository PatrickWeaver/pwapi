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
# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach


def conversation(request, conversation_id):
    # 🚸 Remove this once we are using real times
    time = str(datetime.now())

    if conversation_id:

        response = {
            "messages": [
                {
                    "message": "Hello 1234",
                    "author": "bot",
                    "timestamp": time,
                },
                {
                    "message": "I am a human writing things",
                    "author": "abcd1234",
                    "timestamp": time,
                },
                {
                    "message": "Thank you human for writing things",
                    "author": "bot",
                    "timestamp": time,
                },
                {
                    "message": "Ok I am leaving now.",
                    "author": "abcd1234",
                    "timestamp": time,
                },
            ]
        }

        return JsonResponse(response, safe=False)
    else:
        response = {
            "error": "No Conversation",
        }
        return JsonResponse(response, safe=False)

def guest(request, guest_id):
    if guest_id:
        return HttpResponse(guest_id)
    else:
        response = {
            "error": "No Conversation",
        }
        return JsonResponse(response, safe=False)

def message(request):
    time = str(datetime.now())

    guest = bleach.clean(request.GET.get("guest", ""))
    conversation = bleach.clean(request.GET.get("conversation", ""))

    if guest != "" and conversation != "":
        response = {
            "message": "This is the last message from the last conversation with " + guest + ".",
            "author": "bot",
            "timestamp": time,
        }
    else:
        response = {
            "message": "Hi, I am the bot, it is " + time + ". Thanks for sending a message.",
            "author": "bot",
            "timestamp": time,
        }
    # 🚸 Is this way better?
    # try:
    #     post = Post.objects.get(post_title=title)
    # except Post.DoesNotExist:
    return JsonResponse(response, safe=False)
