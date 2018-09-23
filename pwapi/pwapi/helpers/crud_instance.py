import sys

from functools import partial

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.db import models

from . general import unmodified, remove_hidden_func, get_model_name, log_request, convert_text_field, check_method_type, check_admin, invalid_method
from . responses import error
from . db import find_single_instance, save_object_instance
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

def index_response(
    request=False,
    model=False,
    order_by='?'
):
    
    if not (request and model):
        return error('Invalid request')
    
    # Log the request
    log_request('get', model, 'index', 'all')
    
    # Show these fields on index:
    index_fields = getattr(model, 'index_fields', ['id'])
    
    # get API Key:
    api_key_qs = request.GET.get('api_key', False)
    if api_key_qs:
        api_key = bleach.clean(api_key_qs)
    else:
        api_key = False
    
    # Admin True or False based on api_key
    admin = check_api_key(api_key)
    
    # Get queryset of instances for specified or default page
    # Try/except will deal with any non integer values other than 'all'
    try:
        page = int(bleach.clean(request.GET.get('page', str(default['page']))))
        quantity_qs = request.GET.get('quantity', str(default['quantity']))
        if quantity_qs == 'all':
            end_of_page = None
            start_of_page = None
        else:
            quantity = int(bleach.clean(quantity_qs))
            end_of_page = page * quantity
            start_of_page = end_of_page - quantity
    except ValueError:
        page = default['page']
        quantity = default['quantity']
        end_of_page = page * quantity
        start_of_page = end_of_page - quantity   
  
    
    # Get all instances from DB   
    filter = {}
    if hasattr(model, 'hide_if') and not admin:
        filter[model.hide_if] = False
        
    ordered_instance_objects_qs = model.objects.filter(**filter).order_by(order_by)
    # If not all are requested, scope to quantity and page:
    if (end_of_page != None) and (start_of_page != None):
        ordered_instance_objects_qs = ordered_instance_objects_qs[start_of_page:end_of_page]
    
    # get single instance flow on each object
    modify_each_with = getattr(model, 'index_modify_with', unmodified)
    on_each_instance = partial(single_instance_to_dict, request=request, allowed_fields=index_fields, modify_with=modify_each_with)
    index_list = list(map(
        on_each_instance,
        ordered_instance_objects_qs
    ))
    
    # Get count of items on all pages, exclude hidden if not admin:
    if not admin:
        number_of = model.objects.all().count()
    else:
        key = model.hide_if
        filter_dict = {key: False}
        number_of = model.objects.filter(**filter_dict).count() 
    
    # Create response dict
    model_name = get_model_name(model)
    response = {
        'total_' + model_name:   number_of,
        'page':                  page,
        'admin':                 admin,
        model_name + '_list':    index_list
    } 
    
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(response, safe=False)


    
# Get an existing instance:
def get_instance(
    request=False,
    model=False,
    lookup_field=False,
    lookup_value=False
):
    if not (request and model and lookup_field and lookup_value):
        return error("Invalid request")
      
    # Log the request
    log_request('get', model, lookup_field, lookup_value)
    
    # Limit response to these fields:
    allowed_fields = getattr(model, 'allowed_fields', ['id'])
    
    # get API Key:
    api_key_qs = request.GET.get('api_key', False)
    if api_key_qs:
        api_key = bleach.clean(api_key_qs)
    else:
        api_key = False
    
    # Admin True or False based on api_key
    admin = check_api_key(api_key)
    
    # Check that request uses "GET" method else return error
    required_method_type = "GET"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    # Get single queryset from db else return error
    instance = find_single_instance(model, lookup_field, lookup_value, admin)
    instance_dict = single_instance_to_dict(
      instance,
      request = request,
      allowed_fields = allowed_fields
    )
  
    if instance_dict:
        return JsonResponse(instance_dict, safe=False)
    else:
        return error("Can't find in db.")
 

def single_instance_to_dict(
    instance,
    request = False,
    allowed_fields = False,
    modify_with = False
    
):
    if instance:
        model = type(instance)
        # Get dict without related objects
        instance_dict = instance.__dict__
    else:
        return None
    
    if instance_dict:
        # Remove non-allowed fields from instance_dict
        if not allowed_fields:
            allowed_fields = getattr(model, 'allowed_fields', [])
        instance_dict = remove_non_allowed_fields(instance_dict, allowed_fields)
        
        for field in instance_dict:
        # Convert text fields to html and plaintext (as well as markdown default)
            if model._meta.get_field(field).__class__ is models.TextField and instance_dict[field]:
                instance_dict[field] = convert_text_field(instance_dict[field])
    
    if instance_dict and modify_with:
        # Modify instance dict
        instance_dict = modify_with(instance_dict)
    
    
    if instance_dict:
        # Get dict of only related objects from instance
        related_fields = getattr(model, 'related_fields', [])
        related_objects_dict = get_related_objects(request, related_fields, instance)

    if instance_dict and request:
        instance_dict['api_url'] = instance.get_api_url(request)
        
    if instance_dict:
        #if instance_dict["upload"]:
        #    instance_dict["url"] = instance.upload.url
        return {**instance_dict, **related_objects_dict}

    else:
        return None
    
# Create a new instance:
def new_instance(
    request=False,
    model=False
):

    if not (request and model):
        return error("Invalid Request")
  
    log_request("new", model, 'new', '')
    
    # Limit to/Require these fields:
    allowed_fields = getattr(model, 'allowed_fields', ['id'])
    required_fields = getattr(model, 'required_fields', [])   
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    parsed_body = json.loads(request.body.decode('utf-8'))
    if not parsed_body:
        return False
      
    if 'api_key' in parsed_body:
        admin = check_api_key(parsed_body['api_key'])
    else:
        admin = False
    if not admin:
        return error('Admin only action')
    
    request_dict = check_for_required_and_allowed_fields(model, parsed_body, required_fields, allowed_fields)
    if not request_dict:
        return error("Invalid request") 
      
    object_instance = save_object_instance(model, request_dict)
    if not object_instance:
        return error("Error saving object")
    instance_dict = dict_from_single_object(object_instance, allowed_fields)
    instance_dict["success"] = True
    return JsonResponse(instance_dict, safe=False)
  
# Edit an existing instance
def edit_instance(
    request=False,
    model=False,
    lookup_field=False,
    lookup_value=False
):
      
    if not (request and model and lookup_field and lookup_value):
        return error("Invalid request")
  
    log_request("edit", model, lookup_field, lookup_value)
    
    # Limit to/require these fields:
    allowed_fields = getattr(model, 'allowed_fields', ['id'])
    required_fields = getattr(model, 'required_fields', [])
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    parsed_body = json.loads(request.body.decode('utf-8'))
    if not parsed_body:
        return False
      
    if 'api_key' in parsed_body:
        admin = check_api_key(parsed_body['api_key'])
    else:
        admin = False
    if not admin:
        return error('Admin only action')
      
    ## No required fields because they might not be changing  
    request_dict = check_for_required_and_allowed_fields(model, parsed_body, [], allowed_fields)
    if not request_dict:
          return error("No body in request or incorrect fields")
      
    instance = find_single_instance(model, lookup_field, lookup_value, admin)
    if not instance:
        return error("Can't find in db.")
       
    primary_key_field = model._meta.pk.name
    request_dict[primary_key_field] = instance.pk
    
    # Update each property in the instance that is different in the request_dict
    for i in request_dict:
        if getattr(instance, i) != request_dict[i]:
            try:
                setattr(instance, i, request_dict[i])
            except:
                return error('Error updating instance')  
    
    # Now check for required_fields
    for i in required_fields:
        if not getattr(instance, i):
            return error('Error updating instance')
    
    instance.save()
    if not instance:
        return error("Error saving object")
    
    updated_instance_dict = dict_from_single_object(instance, allowed_fields)
    if not updated_instance_dict:
        return error("Error generating response")
      
    updated_instance_dict["success"] = True
    print(updated_instance_dict)
    return JsonResponse(updated_instance_dict, safe=False)
    
# Delete an existing instance
def delete_instance(
    request=False,
    model=False,
    lookup_field=False,
    lookup_value=False
):
  
    if not (request and model and lookup_field and lookup_value):
        return error("Invalid request")
      
    log_request("delete by", model, lookup_field, lookup_value)
    
    required_method_type = "POST"
    if not check_method_type(request, required_method_type):
        return invalid_method(required_method_type)
      
    parsed_body = json.loads(request.body.decode('utf-8'))
    if not parsed_body:
        return False
      
    if 'api_key' in parsed_body:
        admin = check_api_key(parsed_body['api_key'])
    else:
        admin = False
    if not admin:
        return error('Admin only action')
      
    instance = find_single_instance(model, lookup_field, lookup_value, admin)
    if not instance:
        return error("Can't find in db.")
    instance.delete()
    
    return JsonResponse({'success': True})
  
def dict_from_single_object(instance, allowed_fields):
    try:
        instance_dict = instance.__dict__
        model = type(instance)
        sanitized_instance_dict = remove_non_allowed_fields(instance_dict, allowed_fields)
        return sanitized_instance_dict
    except:
        print("ERROR:")
        print(sys.exc_info())
        return False
      
def check_for_required_and_allowed_fields(model, parsed_body, required_fields = [], allowed_fields = []):
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
def get_related_objects(request, related_fields, instance):
    instance_dict = model_to_dict(instance)
    model = type(instance)
    
    related_keys = list(map(
        lambda rf: rf['key_name'],
        related_fields
    ))

    def related_field_to_dict(model, instance, rf):
        try:
            if model._meta.get_field(rf['field_name']).__class__ is models.ManyToManyField:

                related_single_instance_to_dict = partial(single_instance_to_dict, request=request)

                return sorted(list(map(
                    related_single_instance_to_dict,
                    instance_dict[rf['field_name']]
                )), key=lambda k: k[rf['sort']])
            elif model._meta.get_field(rf['field_name']).__class__ is models.ManyToOneRel:
                print(getattr(instance, rf['field_name']).all())
            else:
                return model_to_dict(getattr(instance, rf['field_name']))
        except:
            related_single_instance_to_dict = partial(single_instance_to_dict, request=request)
            
            return sorted(list(map(
                related_single_instance_to_dict,
                getattr(instance, rf['field_name']).all()
            )), key=lambda k: k[rf['sort']])
          
    related_values = list(map(        
        partial(related_field_to_dict, model, instance),
        related_fields
    ))

    return dict(zip(related_keys, related_values))