from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from people.models import Person
import bleach, bcrypt, sys

from django.forms.models import model_to_dict

from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance
from pwapi.helpers.responses import error, invalid_method
from pwapi.helpers.general import check_method_type, check_api_key


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
        #person_dict["email"] = getattr(i, "email")
        #person_dict["api_key"] = getattr(i, "api_key")
        people_list.append(person_dict)
    print(people_list)
    return JsonResponse(people_list, safe=False)
  
def new_person(request):
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
  
    try:
        parsed_body = json.loads(request.body.decode('utf-8'))
    except:
        return error('no body')
    
    for field in Person.required_fields:
        if field not in parsed_body:
            return error('mising fields')
          
    if 'api_key' in parsed_body:
        admin = check_api_key(parsed_body['api_key'])
    else:
        admin = False
    #if not admin:
    #    return error('Admin only action')
    
    parsed_body['hashed_password'] = bcrypt.hashpw(parsed_body['password'].encode('utf-8'), bcrypt.gensalt())
    try:
        del parsed_body['password']
        del parsed_body['api_key']
    except KeyError:
        return error('cant delete')
      
    person = Person(**parsed_body)
    try:
        person.save()
    except:
        print('ERROR: Can\'t create person.')
        print(sys.exc_info())
        return error('Can\'t create person.')
      
    return JsonResponse(Person.admin_view(person))
    

def authenticate(request):
    error = False
    print(request.body.decode("utf-8"))
    if request.method == "POST":
        if request.body:
            jsonData = json.loads(request.body.decode("utf-8"))
            if jsonData["username"] and jsonData["password"]:
                username = bleach.clean(jsonData["username"])
                password = jsonData["password"]
                try:
                    person = Person.objects.filter(username=username)[0]
                    if bcrypt.checkpw(password.encode('utf-8'), bytes(person.hashed_password)):
                        response = {**Person.admin_view(person), **{'success': True}}
                        return JsonResponse(response, safe=False)
                    else:
                        return JsonResponse({"Error": "Invalid Login"}, safe=False)
                    
                except IndexError:
                    return JsonResponse({"Error": "Invalid Login"}, safe=False)
                except:
                    print(sys.exc_info())
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
