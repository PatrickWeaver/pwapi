from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from people.views import check_api_key

# https://docs.python.org/3/library/json.html
import json

# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach

# General error message for invalid requests:
errorJSON = [{'Error': 'No data for that request.'}]
def error():
    return JsonResponse(errorJSON, safe=False)
  
def log(req_type, model, slug):
    print(req_type + ' ' + str(model.__name__) + ': ' + slug)

def get_instance(model, slug):
    log('get', model, slug)
    instance = find_single_instance_from_slug(model, slug)
    if not instance:
        return error()
    instance_dict = model_to_dict(instance)
    if not instance_dict:
        return error()
    return JsonResponse(instance_dict, safe=False)

  
def new_instance(request, model, slug, required_fields):
    log('new', model, slug)
    instance_dict = instance_dict_from(request, model, required_fields)
    return instance_dict

def find_single_instance_from_slug(model, slug):
    try:
        instance = model.objects.get(slug=slug)
        return instance
    except model.DoesNotExist:
        print('Can\'t find ' + type(model) + ' with slug ' + slug)
        return False
      
def instance_dict_from(request, model, required_fields):
    if not request.body:
        return False
    parsed_body = json.loads(request.body.decode('utf-8'))
    if 'api_key' not in parsed_body:
        return False
    api_key_valid = check_api_key(bleach.clean(parsed_body['api_key']))
    if not api_key_valid:
        return False
    for field in required_fields:
        if field not in parsed_body:
            return False
    instance_dict = {}
    #🚸 Problem that non allowed fields are inserted
    #🚸 Find a way to check if dates are dates
    for field in parsed_body:
        bool = False
        try:
            field_type = model._meta.get_field(field)  
            print(field_type.get_internal_type())
        except:
            pass
        instance_dict[field] = bleach.clean(parsed_body[field])
    return instance_dict
        
    