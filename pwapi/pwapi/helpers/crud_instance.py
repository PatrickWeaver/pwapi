import sys

from functools import partial

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from people.views import check_api_key

from . general import unmodified, remove_hidden_func, get_model_name, validate_body, log_request
from . responses import error
from . db import find_single_instance, save_object_instance

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


def check_method_type(request, type):
    print("Required:", request.method)
    print("Actual:", type)
    if request.method == type:
        return True
    return False
  
def invalid_method(type):
    return error("- Only " + type  + " requests are allowed at this endpoint.")

def index_response(request, model, index_fields, order_by, related_fields=[], modify_each_with=unmodified, hide_except_admin_field=None):
    log_request('get', model, 'all')
    # Pagination
    # Try/except will deal with any non integer values
    try:
        page = int(bleach.clean(request.GET.get("page", str(default['page']))))
        quantity = int(bleach.clean(request.GET.get("quantity", str(default['quantity']))))
    except ValueError:
        page = default['page']
        quantity = default['quantity']
    end_of_page = page * quantity
    start_of_page = end_of_page - quantity
    
    api_key = bleach.clean(request.GET.get("api_key", ""))
    admin_sanitizer = remove_hidden_func(hide_except_admin_field)
    if api_key and check_api_key(api_key):
        admin_sanitizer = unmodified
    
    model_name = get_model_name(model)
    
    all_instances = model.objects.all()
    ordered_instance_objects = all_instances.order_by(order_by)[start_of_page:end_of_page]    
    
    index_list = []
    
    # Add related objects as dictionaries
    # Passed to parent function in related_fields
    get_related_objects_from = partial(get_related_objects, related_fields)
    
    index_list = list(map(
        get_related_objects_from,
        ordered_instance_objects
    ))
    
    # Perform any mutations, and remove hidden unless admin
    def modify_each_instance(instance):
        instance = modify_each_with(instance)
        if hide_except_admin_field:
          if hide_except_admin_field not in instance: 
              return error("Internal error: Admin only eval field passed, but does not exist.")
          instance = admin_sanitizer(instance)
        return instance
    
    modified_index_list = list(map(
        modify_each_instance,
        index_list
    ))
    
    # Remove None items from list that were removed from admin_sanitizer()
    modified_index_list = list(filter((None).__ne__, modified_index_list))
    number_of = len(modified_index_list)
    
    response = {
        'total_' + model_name:   number_of,
        'page':                        page,
        model_name + '_list':          modified_index_list
    } 
    
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(response, safe=False)


    
# Get an existing instance:
def get_instance(request, model, slug, allowed_fields, related_fields=[], modify_with=unmodified, hide_except_admin_field=None):
    log_request('get', model, slug)
    
    required_method_type = "GET"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    instance = find_single_instance(model, "slug", slug)
    if not instance:
        return error("Can't find in db.")
    
    print("((", instance)
    print(type(instance))
    #sanitized_instance_dict = dict_from_single_object(instance, allowed_fields)
    sanitized_instance_dict = get_related_objects(related_fields, instance, allowed_fields)
      
    modified_instance_dict = modify_with(sanitized_instance_dict)
    
    api_key = bleach.clean(request.GET.get("api_key", ""))
    admin_sanitizer = remove_hidden_func(hide_except_admin_field)
    if api_key and check_api_key(api_key):
        admin_sanitizer = unmodified
    admin_sanitized_instance_dict = admin_sanitizer(modified_instance_dict)
    
    if admin_sanitized_instance_dict:
        return JsonResponse(admin_sanitized_instance_dict, safe=False)
    else:
        return error("Can't find in db.")

  
# Create a new instance:
def new_instance(request, model, required_fields, allowed_fields):
    log_request("new", model)
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
    
    request_dict = check_for_required_and_allowed_fields(request, model, required_fields, allowed_fields)
    if not request_dict:
        return error("No body in request or incorrect fields")
      
    object_instance = save_object_instance(model, request_dict)
    if not object_instance:
        return error("Error saving object")
    
    instance_dict = dict_from_single_object(object_instance, allowed_fields)
    
    instance_dict["success"] = True
    return JsonResponse(instance_dict, safe=False)
  
# Edit an existing instance
def edit_instance(request, model, slug, required_fields, allowed_fields):
    log_request("edit", model, slug)
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    request_dict = check_for_required_and_allowed_fields(request, model, required_fields, allowed_fields)
    if not request_dict:
          return error("No body in request or incorrect fields")
      
    instance = find_single_instance(model, "slug", slug)
    if not instance:
        return error("Can't find in db.")
    
    
    primary_key_field = model._meta.pk.name
    request_dict[primary_key_field] = instance.pk
    
    object_instance = save_object_instance(model, request_dict)
    if not object_instance:
        return error("Error saving object")
    
    updated_instance_dict = dict_from_single_object(object_instance, allowed_fields)
    if not updated_instance_dict:
        return error("Error generating response")
      
    updated_instance_dict["success"] = True
    print(updated_instance_dict)
    return JsonResponse(updated_instance_dict, safe=False)
    
# Delete an existing instance
def delete_instance(request, model, key, value):
    log_request("delete by", model, value)
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
    
    instance_dict = check_for_required_and_allowed_fields(request, model)
    if not instance_dict:
        return error("No body in request or incorrect API key")
      
    instance = find_single_instance(model, key, value)
    if not instance:
        return error("Can't find in db.")
    instance.delete()
    
    return JsonResponse({'success': True})

  
  
def dict_from_single_object(instance, allowed_fields):
    try:
        instance_dict = instance.__dict__
        sanitized_instance_dict = remove_non_allowed_fields(instance_dict, allowed_fields)
        return sanitized_instance_dict
    except:
        print("ERROR:")
        print(sys.exc_info())
        return False
      
def check_for_required_and_allowed_fields(request, model, required_fields = [], allowed_fields = ["api_key"]):
    parsed_body = validate_body(request)
    parsed_body_with_valid_types = parsed_dict_from(parsed_body, model)
    sanitized_parsed_body = remove_non_allowed_fields(parsed_body, allowed_fields)
    if sanitized_parsed_body == {}:
        print('Error parsing request body.')
        return False
    for field in required_fields:
        if field not in sanitized_parsed_body:
            return False
    return sanitized_parsed_body
      
def parsed_dict_from(parsed_body, model):
    parsed_dict = {}
    #🚸 Find a way to check if dates are dates
    for field in parsed_body:
        value = bleach.clean(str(parsed_body[field]))
        try:
            field_type = model._meta.get_field(field)  
            model_type = field_type.get_internal_type()
            parsed_dict[field] = parse_non_text_field(model_type, value)    
        except:
            pass
    return parsed_dict
  
def remove_non_allowed_fields(instance_dict, allowed_fields):
    sanitized_instance_dict = {}
    for field in allowed_fields:
        try:
            sanitized_instance_dict[field] = instance_dict[field]
        except:
            print(sys.exc_info())
            print(field, "not provided, using default")
    return sanitized_instance_dict
  
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

# Add related objects as dictionaries
# Passed to parent function in related_fields
def get_related_objects(related_fields, instance, allowed_fields = False):
    instance_dict = model_to_dict(instance)
    
    if allowed_fields:
        instance_dict = remove_non_allowed_fields(instance_dict, allowed_fields)
    
    related_keys = list(map(
        lambda rf: rf["field_name"],
        related_fields
    ))

    def related_field_to_dict(rf):
      
        print("^^", instance)
      
        return list(map(
            model_to_dict,
            instance_dict[rf["field_name"]]
        ))

    related_values = list(map(
      related_field_to_dict,
      related_fields
    ))

    related_dict = dict(zip(related_keys, related_values))
    return {**instance_dict, **related_dict}