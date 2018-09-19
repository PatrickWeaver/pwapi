# https://docs.python.org/3/library/json.html
import json
# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach

from people.views import check_api_key

# Default function for unmodified instance dicts
def unmodified(instance):
  return instance

def remove_hidden_func(field):
    if field:
        def closure(instance):
          if instance[field] == True:
              return None
          return instance

        return closure
    else:
        return unmodified
      
      
def get_model_name(model):
    return str(model.__name__).lower() + 's'

def log_request(req_type, model, slug=""):
  print(req_type, get_model_name(model), ':', slug)
  
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