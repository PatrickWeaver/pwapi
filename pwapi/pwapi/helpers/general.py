from people.views import check_api_key

# https://docs.python.org/3/library/json.html
import json

# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach
# Allow iframe tags and attributes for YouTube videos:
bleach.sanitizer.ALLOWED_TAGS.append(u'iframe')
bleach.sanitizer.ALLOWED_ATTRIBUTES[u'iframe'] = [u'width', u'height', u'src', u'frameborder', u'allow', u'allowfullscreen']
# BeautifulSoup4 is used to get plaintext from HTML (via Markdown)
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

# Markdown is used to parse markdown to HTML to send to Beautiful Soup.
# https://pypi.python.org/pypi/Markdown
from markdown import markdown

# Default function for unmodified instance dicts
def unmodified(instance):
  return instance

def invalid_method(type):
    return error('- Only ' + type  + ' requests are allowed at this endpoint.')

def remove_hidden_func(field):
    if field:
        def closure(instance):
          if instance[field] == True:
              return None
          return instance

        return closure
    else:
        return unmodified
      
      
def get_model_name(model, singular=False):
    plural = 's'
    if singular:
        plural = ''
    return str(model.__name__).lower() + plural

def log_request(req_type, model, lookup_field, lookup_value):
  print(req_type, get_model_name(model), 'by', lookup_field, ':', lookup_value)
  
def convert_text_field(text):
    html = markdown(text, extensions=['markdown.extensions.extra'])
    plaintext = get_plaintext(html, with_links=True)
    return {
        'markdown': text,
        'html': html,
        'plaintext': plaintext
    }
  
def get_plaintext(html_text, with_links=False):
    soup = BeautifulSoup(html_text, 'html5lib')
    if with_links:
        for a in soup.find_all('a'):
            a.append(' (' + a['href'] + ')')
    plaintext = bleach.clean(''.join(soup.findAll(text=True)))
    return plaintext
  
def check_admin(request):
    # Admin status default false, check api_key to set
    admin = False
    if request.method == 'GET':
        api_key_qs = request.GET.get('api_key', False)
        if api_key_qs:
            api_key = bleach.clean(api_key_qs)
        else:
            print('Error: no api_key_qs')
            return False
    elif request.method == 'POST':
        '''
        parsed_body = json.loads(request.body.decode('utf-8'))
        if 'api_key' not in parsed_body:
            return False
        api_key_valid = check_api_key(bleach.clean(parsed_body['api_key']))
        '''
    else:
        # Only GET and POST are valid request methods
        print('Error: invalid request method:', request.method)
        return False
    if api_key:
        admin = check_api_key(api_key)
    return admin
  
def check_method_type(request, type):
    print('Required:', request.method)
    print('Actual:', type)
    if request.method == type:
        return True
    return False
