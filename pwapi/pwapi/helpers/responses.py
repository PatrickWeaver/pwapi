from django.http import JsonResponse

def error(message):
    # General error message for invalid requests:
    errorJSON = [{'Error': 'No data for that request. ' + message}]
    return JsonResponse(errorJSON, safe=False)
  
def invalid_method(type):
    return error('- Only ' + type  + ' requests are allowed at this endpoint.')
