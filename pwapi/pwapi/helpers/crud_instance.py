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

# Allow iframe tags and attributes for YouTube videos:
bleach.sanitizer.ALLOWED_TAGS.append(u'iframe')
bleach.sanitizer.ALLOWED_ATTRIBUTES[u'iframe'] = [u'width', u'height', u'src', u'frameborder', u'allow', u'allowfullscreen']

# Default values:

default = {
    'page': 1,
    'quantity': 5
}

# Default function for unmodified instance dicts
def unmodified(instance):
  return instance


def index_response(request, model, index_fields, order_by, modify_each_with=unmodified):
    log('get', model, 'all')
  
    # Pagination
    try:
        page = int(bleach.clean(request.GET.get("page", str(default['page']))))
        quantity = int(bleach.clean(request.GET.get("quantity", str(default['quantity']))))
    except ValueError:
        page = default['page']
        quantity = default['quantity']
    end_of_page = page * quantity
    start_of_page = end_of_page - quantity
    model_name = str(model.__name__).lower()
    
    all_instances = model.objects.all()
    number_of = all_instances.count()
    ordered_instances = all_instances.order_by(order_by)[start_of_page:end_of_page].values(*index_fields)
    index_list = []
    for i in ordered_instances:
        modified_i = modify_each_with(i)
        index_list.append(modified_i)
    
    response = {
        'total_' + model_name + 's':   number_of,
        'page':                        page,
        model_name + '_list':          index_list
    }
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(response, safe=False)

def error(message):
    # General error message for invalid requests:
    errorJSON = [{'Error': 'No data for that request. ' + message}]
    return JsonResponse(errorJSON, safe=False)
  
def log(req_type, model, slug=""):
    print(req_type + ' ' + str(model.__name__).lower() + ': ' + slug)

# GET Requests:
def get_instance(model, slug, allowed_fields, modify_with=unmodified):
    log('get', model, slug)
    instance = find_single_instance_from_slug(model, slug)
    if not instance:
        return error('Can\'t find in db.')
    instance_dict = model_to_dict(instance)
    if not instance_dict:
        return error('Error parsing data from db.')
    modified_instance_dict = modify_with(instance_dict)
    return JsonResponse(modified_instance_dict, safe=False)

# POST Requests:
def new_instance(request, model, required_fields, allowed_fields):
    if request.method == 'POST':
        log('new', model)
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
    else:
        return error('- Only GET requests are allowed at this endpoint.')
  
# PUT Requests:
def edit_instance(request, model, slug, required_fields, allowed_fields):
    if request.method == 'POST':
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
    else:
        return error('- Only GET requests are allowed at this endpoint.')
    
# DELETE Requests:
def delete_instance(request, model, slug):
    if request.method == 'POST':
        log('delete', model, slug)
        parsed_body = check_for_required_fields(request, [])
        if not parsed_body:
            return error('No body in request or incorrect API key')
        instance = find_single_instance_from_slug(model, slug)
        if not instance:
            return error('Can\'t find in db.')
        instance.delete()
        return JsonResponse({'success': True})
    else:
        return error('- Only GET requests are allowed at this endpoint.')


def find_single_instance_from_slug(model, slug):
    print(type(slug))
    try:
        instance = model.objects.get(slug=slug)
        return instance
    except model.DoesNotExist:
        print('Can\'t find ', model, 'with slug', slug)
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
        value = bleach.clean(str(parsed_body[field]))
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
            print("Not including", field)
    return sanitized_instance_dict
  
def object_instance_from(model, instance_dict):
    object_instance = model(**instance_dict)
    try:
        object_instance.save()
        return object_instance
    except:
        print("ERROR: Can't create object")
        print(sys.exc_info())
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
    