import sys

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from people.views import check_api_key

# https://docs.python.org/3/library/json.html
import json

# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach


def error(message):
    # General error message for invalid requests:
    errorJSON = [{'Error': 'No data for that request. ' + message}]
    return JsonResponse(errorJSON, safe=False)
  
def log(req_type, model, slug):
    print(req_type + ' ' + str(model.__name__) + ': ' + slug)

# GET Requests:
def get_instance(model, slug):
    log('get', model, slug)
    instance = find_single_instance_from_slug(model, slug)
    if not instance:
        return error('Can\'t find in db.')
    instance_dict = model_to_dict(instance)
    if not instance_dict:
        return error('Error parsing data from db.')
    return JsonResponse(instance_dict, safe=False)

# POST Requests:
def new_instance(request, model, slug, required_fields, allowed_fields):
    log('new', model, slug)
    parsed_body = check_for_required_fields(request, required_fields)
    if not parsed_body:
        return error('No body in request or incorrect fields')
    instance_dict = instance_dict_from(parsed_body, model, required_fields)
    sanitized_instance_dict = remove_non_allowed_fields(instance_dict, allowed_fields)
    if sanitized_instance_dict == {}:
        return error('Error parsing request body.')
    object_instance = object_instance_from(model, sanitized_instance_dict)
    if not object_instance:
        return error('Error saving object')
    sanitized_instance_dict['success'] = True
    return JsonResponse(sanitized_instance_dict, safe=False)
  
# PUT Requests:
def edit_instance(request, model, slug, required_fields, allowed_fields):
  log('edit', model, slug)
  parsed_body = check_for_required_fields(request, required_fields)
  if not parsed_body:
        return error('No body in request or incorrect fields')
  instance = find_single_instance_from_slug(model, slug)
  if not instance:
      return error('Can\'t find in db.')
  instance_dict = instance_dict_from(parsed_body, model, required_fields)
  sanitized_instance_dict = remove_non_allowed_fields(instance_dict, allowed_fields)
  if sanitized_instance_dict == {}:
      return error('Error parsing request body.')
  instance = update_instance_using_dict(instance, sanitized_instance_dict)
  instance.save()
  updated_instance_dict = model_to_dict(instance)
  if not updated_instance_dict:
      return error('Error generating response')
  updated_instance_dict['success'] = True
  return JsonResponse(updated_instance_dict, safe=False)
  
    

#def instance_dict_from_model_and_slug(model, slug):  

  
  

def find_single_instance_from_slug(model, slug):
    try:
        instance = model.objects.get(slug=slug)
        return instance
    except model.DoesNotExist:
        print('Can\'t find ' + type(model) + ' with slug ' + slug)
        return False
      
def check_for_required_fields(request, required_fields):
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
    return parsed_body
      
def instance_dict_from(parsed_body, model, required_fields):
    instance_dict = {}
    #🚸 Problem that non allowed fields are inserted
    #🚸 Find a way to check if dates are dates
    for field in parsed_body:
        value = bleach.clean(parsed_body[field])
        try:
            field_type = model._meta.get_field(field)  
            model_type = field_type.get_internal_type()
            instance_dict[field] = parse_non_text_field(model_type, value)    
        except:
            pass
        
    return instance_dict
  
def remove_non_allowed_fields(instance_dict, allowed_fields):
    sanitized_instance_dict = {}
    for field in allowed_fields:
        try:
            sanitized_instance_dict[field] = instance_dict[field]
        except:
            sanitized_instance_dict[field] = None
    return sanitized_instance_dict
  
def object_instance_from(model, instance_dict):
    object_instance = model(**instance_dict)
    try:
        object_instance.save()
        return object_instance
    except:
        print("ERROR")
        print(sys.exc_info()[0])
        return False
  
def parse_non_text_field(field_type, value):
    if field_type == 'BooleanField':
        if value.upper() == 'TRUE':
            return True
        elif value.upper() == 'FALSE':
            return False
        else:
            return error('Boolean field not true or false')
    else:
      return value
    
def update_instance_using_dict(instance, instance_dict):
    for key, value in instance_dict.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
        else:
            print('Instance does not have attribute ' + key)
    return instance
    