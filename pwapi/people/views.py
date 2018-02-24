from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from people.models import Person
import bleach

#from django.forms.models import model_to_dict

# https://docs.python.org/3/library/json.html
import json

errorJSON = [{"Error": "No data for that request."}]

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
    error = False
    if request.method == "POST":
        if request.body:
            jsonData = json.loads(request.body)
            if jsonData["username"]:
                username = bleach.clean(jsonData["username"])
            if jsonData["password"]:
                password = bleach.clean(jsonData["password"])

            person_dict = {
                "id": 1234,
                "username": username,
                "name": username,
                "email": username + "@example.com",
                "api_key": "abc_123"
            }
        else:
            error = True

        return JsonResponse(person_dict, safe=False)
    else:
        instructions = {
          0: "New post must be submitted as POST request.",
          1: {
            "Required Fields:": {
              0: "username",
              1: "password"
            }
          }

        }

        return JsonResponse(instructions, safe=False)

    #error = True
    if error == True:
        return JsonResponse(errorJSON, safe=False)
