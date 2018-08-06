from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from portfolio.models import Tag, Image, Project
from people.views import check_api_key

from datetime import datetime
# https://docs.python.org/3/library/json.html
import json
# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach
# Allow iframe tags and attributes for YouTube videos:
bleach.sanitizer.ALLOWED_TAGS.append(u'iframe')
bleach.sanitizer.ALLOWED_ATTRIBUTES[u'iframe'] = [u'width', u'height', u'src', u'frameborder', u'allow', u'allowfullscreen']

# General error message for invalid requests:
errorJSON = [{'Error': 'No data for that request.'}]

def index(request):
    return HttpResponse('Portfolio')

  
#  --- --- --- --- --- --- #
# - - - - PROJECTS - - - - #
# --- --- --- --- --- ---  #

def projects(request):
    response = {'ok': 'ok'}
    # No pagination for now:
    # See blog.views.posts for example

    all_projects = Project.objects.all()
    number_of_projects = all_projects.count()
    projects = all_projects.order_by('-start_date').values('name', 'slug', 'description', 'start_date', 'end_date', 'project_url', 'status_id')
    index_list = []
    for project in projects:
        index_project = {
            'name':         project['name'],
            'slug':         project['slug'],
            'description':  project['description'],
            'start_date':   project['start_date'],
            'end_date':     project['end_date'],
            'project_url':  project['project_url'],
            'status_id':    project['status_id'],
        }
        index_list.append(index_project)
    response = {
        'total_projects':  number_of_projects,
        'projects_list':   index_list,
    }
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(response, safe=False)

def project(request, slug):
    print(request.method + ': ' + request.path);
    if request.method == 'GET':
        return get_project(request, slug)
    elif request.method == 'POST':
        return new_project(request, slug)
    elif request.method == 'PUT':
        return edit_project(request, slug)
    elif request.method == 'DELETE':
        return delete_project(request, slug)

def get_project(request, slug):
    print('get_project ' + slug)
    project = find_project_from_slug(slug)
    if not project:
        return JsonResponse(errorJSON, safe=False)
    project_dict = project_dict_from_project(project)
    if project_dict == {}:
        return JsonResponse(errorJSON, safe=False)
    else:
        response = project_dict
        return JsonResponse(response, safe=False)

def new_project(request, slug):
    project_dict = project_dict_from_request(request)
    if not project_dict:
        return JsonResponse(errorJSON, safe=False)
    project = project_from_project_dict(project_dict)
    project_response = new_or_edited_project_response_from_project(project)
    if not project_response:
        return JsonResponse(errorJSON, safe=False)
    return JsonResponse(project_response, safe=False)
      
def find_project_from_slug(slug):
    try:
        project = Project.objects.get(slug=slug)
        return project
    except Project.DoesNotExist:
        return False

def project_dict_from_project(project):
    project_dict = {}
    project_dict['name'] = getattr(project, 'name')
    project_dict['slug'] = getattr(project, 'slug')
    project_dict['description'] = getattr(project, 'description')
    project_dict['start_date'] = getattr(project, 'start_date')
    project_dict['end_date'] = getattr(project, 'end_date')
    project_dict['project_url'] = getattr(project, 'project_url')
    project_dict['source_url'] = getattr(project, 'source_url')
    project_dict['status_id'] = getattr(project, 'status_id')
    project_dict = expand_project(project_dict)
    return project_dict


def expand_project(project):
    #html_body = markdown(project["description"], extensions=["markdown.extensions.extra"])
    #post["html_body"] = html_body
    #plaintext_body = get_plaintext(html_body)
    #post["plaintext_body"] = plaintext_body
    return project

def project_dict_from_request(request):
    if not request.body:
        return False
    jsonData = json.loads(request.body.decode('utf-8'))
    if 'name' not in jsonData:
        return False
    if 'api_key' not in jsonData:
        return False
    api_key_valid = check_api_key(bleach.clean(jsonData["api_key"]))
    if not api_key_valid:
        return False
    # Might be better to set these defaults for title and post_date in the model?
    name = ''
    slug = ''
    description = ''
    start_date = None
    end_date = None
    project_url = ''
    source_url = ''
    status_id = False
    if 'name' in jsonData:
        name = bleach.clean(jsonData['name'])
    if 'slug' in jsonData:
        slug = bleach.clean(jsonData['slug'])
    if 'description' in jsonData:
        description = bleach.clean(jsonData['description'])
    if 'project_url' in jsonData:
        project_url = bleach.clean(jsonData['project_url'])
    if 'source_url' in jsonData:
        source_url = bleach.clean(jsonData['source_url'])
    if 'status_id' in jsonData:
        status_id = bleach.clean(jsonData['status_id'])

    #🚸 Find a way to check if it's a date.
    start_date = datetime.now()
    if 'start_date' in jsonData and len(jsonData['start_date']) > 2:
        start_date = bleach.clean(jsonData['start_date'])
    end_date = datetime.now()
    if 'end_date' in jsonData and len(jsonData['end_date']) > 2:
        end_date = bleach.clean(jsonData['end_date'])
    project_dict = {
        'name':         name,
        'slug':         slug,
        'description':  description,
        'start_date':   start_date,
        'end_date':     end_date,
        'project_url':  project_url,
        'source_url':   source_url,
        'status_id':    status_id
    }
    return project_dict

def project_from_project_dict(project_dict):
    if not project_dict:
        return False
    project = Project(**project_dict)
    project.save()
    return project

def new_or_edited_project_response_from_project(project):
    response = {
        'success': True,
        'name': project.name,
        'slug': project.slug,
        'description': project.description,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'project_url': project.project_url,
        'source_url': project.source_url,
        'status_id': project.status_id
    }
    return response

def edit_project(request, slug):
    print('edit_project ' + slug)
    project = find_project_from_slug(slug)
    project_dict = project_dict_from_request(request)
    if not project_dict:
        return JsonResponse(errorJSON, safe=False)
    project = update_project_from_dict(project, project_dict)
    project.save()
    project_response = new_or_edited_project_response_from_project(project)
    if not project_response:
        return JsonResponse(errorJSON, safe=False)
    return JsonResponse(project_response, safe=False)

def update_project_from_dict(project, project_dict):
    for key, value in project_dict.items():
        if hasattr(project, key):
            setattr(project, key, value)
        else:
            print("project does not have attribute " + key)
    return project

def delete_project(request, slug):
    project = find_project_from_slug(slug)
    project.delete()
    return JsonResponse({'success': True})
  

#  --- --- --- --- --- --- #
# - - - - - TAGS - - - - - #
# --- --- --- --- --- ---  #

def tags(request):
    response = {'ok': 'ok'}
    # No pagination for now:
    # See blog.views.posts for example
    
    all_tags = Tag.objects.all()
    number_of_tags = all_tags.count()
    tags = all_tags.order_by('name').values('name', 'slug', 'color', 'status', 'created_date')
    index_list = []
    for tag in tags:
        index_tag = {
            'name':         tag['name'],
            'slug':         tag['slug'],
            'color':        tag['color'],
            'status':       tag['status'],
            'created_date': tag['created_date'],
        }
        index_list.append(index_tag)
    response = {
        'total_tags': number_of_tags,
        'tags_list':  index_list,
    }
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(response, safe=False)
  
def tag(request, slug):
    print(request.method + ': ' + request.path);
    if request.method == 'GET':
        return get_tag(request, slug)
    elif request.method == 'POST':
        return new_tag(request, slug)
    elif request.method == 'PUT':
        return edit_tag(request, slug)
    elif request.method == 'DELETE':
        return delete_tag(request, slug)
      

def get_tag(request, slug):
    print('get_tag ' + slug)
    tag = find_tag_from_slug(slug)
    if not tag:
        return JsonResponse(errorJSON, safe=False)
    tag_dict = tag_dict_from_tag(tag)
    if tag_dict == {}:
        return JsonResponse(errorJSON, safe=False)
    else:
        response = tag_dict
        return JsonResponse(response, safe=False)
  
def new_tag(request, slug):
    print('new_tag ' + slug)
    tag_dict = tag_dict_from_request(request)
    if not tag_dict:
        return JsonResponse(errorJSON, safe=False)
    tag = tag_from_tag_dict(tag_dict)
    tag_response = new_or_edited_tag_response_from_tag(tag)
    if not tag_response:
        return JsonResponse(errorJSON, safe=False)
    return JsonResponse(tag_response, safe=False)
  
def edit_tag(request, slug):
    print('edit_tag ' + slug)
    tag = find_tag_from_slug(slug)
    tag_dict = tag_dict_from_request(request)
    if not tag_dict:
        return JsonResponse(errorJSON, safe=False)
    tag = update_tag_from_dict(tag, tag_dict)
    tag.save()
    tag_response = new_or_edited_tag_response_from_tag(tag)
    if not tag_response:
        return JsonResponse(errorJSON, safe=False)
    return JsonResponse(tag_response, safe=False)
  
  
def delete_tag(request, slug):
    tag = find_tag_from_slug(slug)
    tag.delete()
    return JsonResponse({'success': True})


def find_tag_from_slug(slug):
    try:
        tag = Tag.objects.get(slug=slug)
        return tag
    except Tag.DoesNotExist:
        return False
      
def tag_dict_from_tag(tag):
    tag_dict = {}
    tag_dict['id'] = getattr(tag, 'id')
    tag_dict['name'] = getattr(tag, 'name')
    tag_dict['slug'] = getattr(tag, 'slug')
    tag_dict['color'] = getattr(tag, 'color')
    tag_dict['status'] = getattr(tag, 'status')
    tag_dict['created_date'] = getattr(tag, 'created_date')
    return tag_dict
  
def tag_dict_from_request(request):
    if not request.body:
        return False
    jsonData = json.loads(request.body.decode('utf-8'))
    if 'name' not in jsonData:
        return False
    if 'status' not in jsonData:
        return False
    if 'color' not in jsonData:
        return False
    if 'api_key' not in jsonData:
        return False
    api_key_valid = check_api_key(bleach.clean(jsonData["api_key"]))
    if not api_key_valid:
        return False
    # Might be better to set these defaults for title and post_date in the model?
    name = ''
    slug = ''
    color = ''
    status = False
    if 'name' in jsonData:
        name = bleach.clean(jsonData['name'])
    if 'slug' in jsonData:
        slug = bleach.clean(jsonData['slug'])
    if 'color' in jsonData:
        color = bleach.clean(jsonData['color'])
    if 'status' in jsonData:
        status = bleach.clean(jsonData['status'])
        if status.upper() == "TRUE":
            status = True
        else:
            status = False

    tag_dict = {
        'name':         name,
        'slug':         slug,
        'color':        color,
        'status':       status,
    }
    
    return tag_dict
  
def tag_from_tag_dict(tag_dict):
    if not tag_dict:
        return False
    tag = Tag(**tag_dict)
    tag.save()
    return tag
  
def new_or_edited_tag_response_from_tag(tag):
    response = {
        'success': True,
        'id':   tag.id,
        'name': tag.name,
        'slug': tag.slug,
        'color': tag.color,
        'status': tag.status,
        'created_date': tag.created_date,
    }
    return response
  
def update_tag_from_dict(tag, tag_dict):
    for key, value in tag_dict.items():
        if hasattr(tag, key):
            setattr(tag, key, value)
        else:
            print("tag does not have attribute " + key)
    return tag