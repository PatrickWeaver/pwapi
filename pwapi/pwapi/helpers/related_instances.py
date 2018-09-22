from django.forms.models import model_to_dict

from django.http import JsonResponse

from . general import get_model_name, invalid_method
from . responses import error
from . db import find_single_instance, save_object_instance

def add_child_to(
    request=False,
    parent_model=False,
    child_model=False,
    parent_key=False,
    parent_identifier_value=False,
    child_field_name_on_parent=False
):
  
    if not (request and parent_model and child_model and parent_key and parent_identifier_value and child_field_name_on_parent):
        return error('Invalid request')
  
    def get_modify_with(parent_instance, child_field_name_on_parent):
      return getattr(parent_instance, child_field_name_on_parent).add
    
    return modify_child_on(request, parent_model, child_model, parent_key, parent_identifier_value, child_field_name_on_parent, get_modify_with)
  
  
def remove_child_from(
    request=False,
    parent_model=False,
    child_model=False,
    parent_key=False,
    parent_identifier_value=False,
    child_field_name_on_parent=False
):
  
    if not (request and parent_model and child_model and parent_key and parent_identifier_value and child_field_name_on_parent):
        return error('Invalid request')
  
    def get_modify_with(parent_instance, child_field_name_on_parent):
      return getattr(parent_instance, child_field_name_on_parent).remove
    
    return modify_child_on(request, parent_model, child_model, parent_key, parent_identifier_value, child_field_name_on_parent, get_modify_with)
    
    
def modify_child_on(request, parent_model, child_model, parent_key, parent_identifier_value, child_field_name_on_parent, get_modify_with):
  
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
            
    parent_instance = find_single_instance(parent_model, parent_key, parent_identifier_value)
    if not parent_instance:
        return error(parent_model.__name__ + " not found")
      
    try:
        child_identifier = parsed_body["identifier"]
        child_identifier_value = parsed_body["value"]
    except:
        return error('No identifier provided')

    try:
        child_instance = find_single_instance(child_model, child_identifier, child_identifier_value)
        modify_with = get_modify_with(parent_instance, child_field_name_on_parent)
        modify_with(child_instance)
    except:
        print(sys.exc_info())
        return error('Error adding or removing child')
    
    # Should generalize this:
    updated_parent_instance_dict = model_to_dict(parent_instance)
    if not updated_parent_instance_dict:
        return error('Error generating response')
    children_dicts = []
    for child in updated_parent_instance_dict[child_field_name_on_parent]:
        children_dicts.append(model_to_dict(child))
    updated_parent_instance_dict[child_field_name_on_parent] = children_dicts
    updated_parent_instance_dict['success'] = True
    return JsonResponse(updated_parent_instance_dict, safe=False)