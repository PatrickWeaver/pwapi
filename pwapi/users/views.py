from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from users.models import User

from django.forms.models import model_to_dict

# https://docs.python.org/3/library/json.html
import json

def users(request):
    users = User.objects.all()
    users_list = []
    for i in users:
        user_dict = {}
        user_dict["username"] = getattr(i, "username")
        user_dict["name"] = getattr(i, "name")
        user_dict["email"] = getattr(i, "email")
        user_dict["api_key"] = getattr(i, "api_key")
        users_list.append(user_dict)
    print(users_list)
    return JsonResponse(users_list, safe=False)
