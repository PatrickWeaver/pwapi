from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from people.models import Person
import bleach

from django.forms.models import model_to_dict

# https://docs.python.org/3/library/json.html
import json

errorJSON = [{"Error": "No data for that request."}]

def people(request):
    people = Person.objects.all()
    people_list = []
    for i in people:
        person_dict = {}
        person_dict["username"] = getattr(i, "username")
        #person_dict["password"] = getattr(i, "password")
        person_dict["name"] = getattr(i, "name")
        #person_dict["email"] = getattr(i, "email")
        #person_dict["api_key"] = getattr(i, "api_key")
        people_list.append(person_dict)
    print(people_list)
    return JsonResponse(people_list, safe=False)

def authenticate(request):
    error = False
    print(request.body)
    if request.method == "POST":
        if request.body:
            jsonData = json.loads(request.body)
            if jsonData["username"] and jsonData["password"]:
                username = bleach.clean(jsonData["username"])
                password = jsonData["password"]
                person = Person.objects.filter(username=username)[0]
                if person.password == password:

                    person_dict = {
                        "id": person.id,
                        "username": person.username,
                        "name": person.name,
                        "email": person.email,
                        "api_key": person.api_key,
                        "type": "admin"
                    }
                    return JsonResponse(person_dict, safe=False)
                else:
                    return JsonResponse({"Error": "Invalid Login"}, safe=False)

    instructions = {
      0: "New post must be submitted as POST request with a json body.",
      1: {
        "Required Fields:": {
          0: "username",
          1: "password"
        }
      }

    }
    return JsonResponse(instructions, safe=False)

def check_api_key(api_key):
    print("CHECKING API KEY")
    person_array = Person.objects.filter(api_key=api_key)
    if len(person_array) < 1:
        print("AUTH ERROR: PERSON NO FOUND OR INVALID API KEY")
        return False
    person = person_array[0]
    # Eventually here we should check if they are an admin or if they have permissions to post to the blog
    if False:
        print("FALSE IN CHECK API KEY")
    #if not (getattr(person, "type") == "admin"):
        return False
    # API Key is valid, maybe make this more complicated at some point:
    print("API KEY VALID")
    return True
