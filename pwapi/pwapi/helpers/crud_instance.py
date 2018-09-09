import sys

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from people.views import check_api_key

from . general import unmodified

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

def get_model_name(model):
    return str(model.__name__).lower() + 's'

def index_response(request, model, index_fields, order_by, modify_each_with=unmodified):
    log('get', model, 'all')
  
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
    
    model_name = get_model_name(model)
    
    all_instances = model.objects.all()
    number_of = all_instances.count()
    ordered_instances = all_instances.order_by(order_by)[start_of_page:end_of_page].values(*index_fields)
    index_list = []
    for i in ordered_instances:
        modified_i = modify_each_with(i)
        if modified_i:
            index_list.append(modified_i)
    
    response = {
        'total_' + model_name:   number_of,
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
    print(req_type, get_model_name(model), ':', slug)

def check_method_type(request, type):
    print("Required:", request.method)
    print("Actual:", type)
    if request.method == type:
        return True
    return False
  
def invalid_method(type):
    return error("- Only " + type  + " requests are allowed at this endpoint.")
    
# GET Requests:
def get_instance(request, model, slug, allowed_fields, modify_with=unmodified):
    log('get', model, slug)
    
    required_method_type = "GET"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    instance = find_single_instance_from(model, "slug", slug)
    if not instance:
        return error("Can\'t find in db.")
      
    sanitized_instance_dict = dict_from_single_object(instance, allowed_fields)
      
    modified_instance_dict = modify_with(sanitized_instance_dict)
    
    return JsonResponse(modified_instance_dict, safe=False)

  
# POST Requests:
def new_instance(request, model, required_fields, allowed_fields):
    log("new", model)
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
    
    request_dict = check_for_required_and_allowed_fields(request, model, required_fields, allowed_fields)
    if not request_dict:
        return error("No body in request or incorrect fields")
      
    object_instance = object_instance_from(model, request_dict)
    if not object_instance:
        return error("Error saving object")
    
    instance_dict = dict_from_single_object(object_instance, allowed_fields)
    
    instance_dict["success"] = True
    return JsonResponse(instance_dict, safe=False)
  
# PUT Requests:
def edit_instance(request, model, slug, required_fields, allowed_fields):
    log("edit", model, slug)
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    request_dict = check_for_required_and_allowed_fields(request, model, required_fields, allowed_fields)
    if not request_dict:
          return error("No body in request or incorrect fields")
      
    instance = find_single_instance_from(model, "slug", slug)
    if not instance:
        return error("Can't find in db.")

    updated_instance = update_instance_using_dict(instance, request_dict)
    if not updated_instance:
        return error("Error saving updated object")
    
    updated_instance_dict = dict_from_single_object(updated_instance, allowed_fields)
    if not updated_instance_dict:
        return error("Error generating response")
      
    updated_instance_dict["success"] = True
    print(updated_instance_dict)
    return JsonResponse(updated_instance_dict, safe=False)
    
# DELETE Requests:
def delete_instance(request, model, key, value):
    log("delete by", model, value)
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
    
    instance_dict = check_for_required_and_allowed_fields(request, model)
    if not instance_dict:
        return error("No body in request or incorrect API key")
      
    instance = find_single_instance_from(model, key, value)
    if not instance:
        return error("Can't find in db.")
    instance.delete()
    
    return JsonResponse({'success': True})

def find_single_instance_from(model, lookup_key, lookup_value):
    try:
        filter_dict = {lookup_key: lookup_value}
        instance = model.objects.get(**filter_dict)
        return instance
    except:
        print("ERROR:")
        print(sys.exc_info())
        return False

def dict_from_single_object(instance, allowed_fields):
    try:
        instance_dict = instance.__dict__
        sanitized_instance_dict = remove_non_allowed_fields(instance_dict, allowed_fields)
        return sanitized_instance_dict
    except:
        print("ERROR:")
        print(sys.exc_info())
        return False
      
def validate_body(request):
    if not request.body:
        return False
    parsed_body = json.loads(request.body.decode("utf-8"))
    if "api_key" not in parsed_body:
        return False
    api_key_valid = check_api_key(bleach.clean(parsed_body["api_key"]))
    if not api_key_valid:
        return False
    return parsed_body
      
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
  

  
def object_instance_from(model, instance_dict):
    object_instance = model(**instance_dict)
    try:
        object_instance.save()
        return object_instance
    except:
        print("ERROR: Can't create object.")
        print(sys.exc_info())
        return False

    
def update_instance_using_dict(instance, instance_dict):
    for key, value in instance_dict.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
        else:
            print('Instance does not have attribute ' + key)
    try:
        instance.save()
        return instance
    except:
        print("Error: Can't save updated object.")
        print(sys.exc_info())
        return False

def add_child_to(request, parent_model, child_model, parent_key, parent_identifier_value):
    def get_modify_with(parent_instance, child_model_name):
      return getattr(parent_instance, child_model_name).add
    return modify_child_on(request, parent_model, child_model, parent_key, parent_identifier_value, get_modify_with)
  
def remove_child_from(request, parent_model, child_model, parent_key, parent_identifier_value):
    def get_modify_with(parent_instance, child_model_name):
      return getattr(parent_instance, child_model_name).remove
    return modify_child_on(request, parent_model, child_model, parent_key, parent_identifier_value, get_modify_with)
    
    
def modify_child_on(request, parent_model, child_model, parent_key, parent_identifier_value, get_modify_with):
    child_model_name = get_model_name(child_model)
    parsed_body = validate_body(request)
            
    parent_instance = find_single_instance_from(parent_model, parent_key, parent_identifier_value)
    if not parent_instance:
        return errror(parent_model__name__ + " not found")
      
    try:
        child_identifier = parsed_body["identifier"]
        child_identifier_value = parsed_body["value"]
    except:
        return error('No identifier provided')

    try:
        child_instance = find_single_instance_from(child_model, child_identifier, child_identifier_value)
        modify_with = get_modify_with(parent_instance, child_model_name)
        modify_with(child_instance)
    except:
        print(sys.exc_info())
        return error('Error adding or removing child')
    
    # Should generalize this:
    updated_parent_instance_dict = model_to_dict(parent_instance)
    if not updated_parent_instance_dict:
        return error('Error generating response')
    children_dicts = []
    for child in updated_parent_instance_dict[child_model_name]:
        children_dicts.append(model_to_dict(child))
    updated_parent_instance_dict[child_model_name] = children_dicts
    updated_parent_instance_dict['success'] = True
    print(updated_parent_instance_dict)
    return JsonResponse(updated_parent_instance_dict, safe=False)