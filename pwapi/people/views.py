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
