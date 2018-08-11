from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from portfolio.models import Tag, Image, Project
from pwapi.helpers.crud_instance import get_instance, new_instance, edit_instance, delete_instance

# https://docs.python.org/3/library/json.html
import json

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
    
    required_fields = ['name']
    allowed_fields = ['slug', 'description', 'start_date', 'end_date', 'project_url', 'source_url', 'status_id'] + required_fields  
    return crud_response(request, Project, slug, required_fields, allowed_fields)

  

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
    
    required_fields = ['name', 'color', 'slug']
    allowed_fields = ['status'] + required_fields
    
    return crud_response(request, Tag, slug, required_fields, allowed_fields)
      
    
    
def crud_response(request, model, slug, required_fields, allowed_fields):
    if request.method == 'GET':
        return get_instance(model, slug)
    elif request.method == 'POST':
        return new_instance(request, model, slug, required_fields, allowed_fields)
    elif request.method == 'PUT':
        return edit_instance(request, model, slug, required_fields, allowed_fields)
    elif request.method == 'DELETE':
        return delete_instance(request, model, slug)