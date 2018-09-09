from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from portfolio.models import Tag, Image, Project
from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance, add_children_to

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
    index_fields = [
        'name',
        'slug',
        'description',
        'start_date',
        'end_date',
        'sort_date',
        'project_url',
        'status_id'
    ] # Add: cover_photo_id
    order_by = '-sort_date'
    return index_response(request, Project, index_fields, order_by)
  
project_required_fields = ['name']
project_allowed_fields = [
    'slug',
    'description',
    'start_date',
    'end_date',
    'sort_date',
    'project_url',
    'source_url',
    'status_id'
] + project_required_fields

def get_project(request, slug):
    return get_instance(request, Project, slug, project_allowed_fields)

def new_project(request):
    return new_instance(request, Project, project_required_fields, project_allowed_fields)
  
def edit_project(request, slug):
    return edit_instance(request, Project, slug, project_required_fields, project_allowed_fields)
  
def delete_project(request, slug):
    return delete_instance(request, Project, "slug", slug)
    

#  --- --- --- --- --- --- #
# - - - - - TAGS - - - - - #
# --- --- --- --- --- ---  #

def tags(request):   
    index_fields = ['name', 'slug', 'color', 'status', 'created_date']
    order_by = 'name'
    return index_response(request, Tag, index_fields, order_by)

tag_required_fields = ['name', 'color', 'slug']
tag_allowed_fields = ['status'] + tag_required_fields 
  
def get_tag(request, slug):
    return get_instance(request, Tag, slug, tag_allowed_fields)
  
def new_tag(request):
    return new_instance(request, Tag, tag_required_fields, tag_allowed_fields)
      
def edit_tag(request, slug):
    return edit_instance(request, Tag, slug, tag_required_fields, tag_allowed_fields)
  
def delete_tag(request, slug):
    return delete_instance(request, Tag, "slug", slug)


#  --- --- --- --- --- --- #
# - - - - IMAGES - - - - - #
# --- --- --- --- --- ---  #

def images(request, project, id):
    pass
'''
    index_fields = ['url', 'caption', 'cover']
    order_by = 'url'
    return index_response(request, Image, index_fields, order_by)
'''

#  --- --- --- --- --- --- #
# - - PROJECT <-> TAG  - - #
# --- --- --- --- --- ---  #

def add_tags_to_project(request, project_slug):
    return add_children_to(request, Project, Tag, "slug", project_slug)
  
def remove_tags_from_project(request, slug):
    return remove_children_from(request, Project, Tag, project_slug)