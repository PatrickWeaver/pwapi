from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from people.models import Person

#from django.forms.models import model_to_dict

# https://docs.python.org/3/library/json.html
import json

def people(request):
    people = Person.objects.all()
    people_list = []
    for i in people:
        person_dict = {}
        person_dict["username"] = getattr(i, "username")
        person_dict["name"] = getattr(i, "name")
        person_dict["email"] = getattr(i, "email")
        person_dict["api_key"] = getattr(i, "api_key")
        people_list.append(person_dict)
    print(people_list)
    return JsonResponse(people_list, safe=False)

def authenticate(request):
    #username = bleach.clean(request.GET.get("username", ""))
    #password = bleach.clean(request.Get.get("password", ""))

    person_dict = {
        "username": "pw-test",
        "name": "Patrick Weaver (test)",
        "email": "pjpweaver@gmail.com-test",
        "api_key": "abc_123"
    }

    return JsonResponse(person_dict, safe=False)
