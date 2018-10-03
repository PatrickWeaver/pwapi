from people.models import Person

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
    html_soup = BeautifulSoup(html, 'html5lib')
    for a in html_soup.find_all('a'):
        a['target'] = '_blank'
    html = str(html_soup)
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
  
def check_api_key(api_key):
    if not api_key:
        return False
    print("CHECKING API KEY:", api_key)
    person_array = Person.objects.filter(api_key=api_key)
    if len(person_array) < 1:
        print("AUTH ERROR: PERSON NOT FOUND OR INVALID API KEY")
        return False
    person = person_array[0]
    # Eventually here we should check if they are an admin or if they have permissions to post to the blog
    if False:
        print("FALSE IN CHECK API KEY")
    #if not (getattr(person, "type") == "admin"):
        return False
    # API Key is valid, maybe make this more complicated at some point:
    print("API KEY VALID")
    return True
