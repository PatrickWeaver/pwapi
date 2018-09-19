from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from portfolio.models import Tag, Image, Project
from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance
from pwapi.helpers.related_instances import add_child_to, remove_child_from
from pwapi.helpers.general import unmodified, get_plaintext

from people.views import check_api_key

# https://docs.python.org/3/library/json.html
import json
import bleach

# Markdown is used to parse markdown to HTML to send to Beautiful Soup.
# https://pypi.python.org/pypi/Markdown
from markdown import markdown

# General error message for invalid requests:
errorJSON = [{'Error': 'No data for that request.'}]

project_related_fields = [
    {
        "field_name": "tags",
        "related_name": "project_tags"
    },
    {
        "field_name": "status",
        "relateed_name": "project_status"
    }
]


def index(request):
    return HttpResponse('<h1>Portfolio</h1><ul><li><a href="projects">Projects</a></li><li><a href="tags">Tags</a></li></ul>')

  
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
        'source_url',
        'is_hidden'
      
    ] # project_related_fields also added
    # Add: cover_photo_id
    
    order_by = '-sort_date'
    return index_response(request, Project, index_fields, order_by, related_fields=project_related_fields)

  
project_required_fields = [
    'name',
    'status_id'
]
project_allowed_fields = [
    'slug',
    'description',
    'start_date',
    'end_date',
    'sort_date',
    'project_url',
    'source_url',
    'is_hidden',
] + project_required_fields # project_related_fields also added later

def get_project(request, slug):
    return get_instance(request, Project, slug, project_allowed_fields, related_fields=project_related_fields)

def new_project(request):
    return new_instance(request, Project, project_required_fields, project_allowed_fields)
  
def edit_project(request, slug):
    return edit_instance(request, Project, slug, project_required_fields, project_allowed_fields)
  
def delete_project(request, slug):
    return delete_instance(request, Project, "slug", slug)
def delete_project_by_id(request, id):
    return delete_instance(request, Project, "id", id)
    

#  --- --- --- --- --- --- #
# - - - - - TAGS - - - - - #
# --- --- --- --- --- ---  #

def modify_new_tags(request_dict):
    if not request_dict["status"]:
        request_dict["color"] = None
        request_dict["name"] = request_dict["name"].lower()
    return request_dict

def tags(request):   
    index_fields = ['name', 'slug', 'color', 'status', 'created_date', 'id']
    order_by = 'name'
    return index_response(request, Tag, index_fields, order_by)

tag_required_fields = ['name']
tag_allowed_fields = ['status', 'slug', 'color'] + tag_required_fields
  
def get_tag(request, slug):
    return get_instance(request, Tag, slug, tag_allowed_fields)
  
def new_tag(request):
    return new_instance(request, Tag, tag_required_fields, tag_allowed_fields, modify_with=modify_new_tags)
      
def edit_tag(request, slug):
    return edit_instance(request, Tag, slug, tag_required_fields, tag_allowed_fields)
  
def delete_tag(request, slug):
    return delete_instance(request, Tag, "slug", slug)
def delete_tag_by_id(request, id):
    return delete_instance(request, Tag, "id", id)


#  --- --- --- --- --- --- #
# - - - - IMAGES - - - - - #
# --- --- --- --- --- ---  #

def images(request):
    index_fields = ['url', 'caption', 'cover', 'uuid', 'created_date', 'project']
    order_by = 'project'
    return index_response(request, Image, index_fields, order_by)

image_required_fields = ['url', 'project']
image_allowed_fields = ['caption', 'cover'] + image_required_fields
  
def get_image(request, uuid):
    return get_instance(request, Image, uuid, image_allowed_fields)
  
def new_image(request):
    return new_instance(request, Image, image_required_fields, image_allowed_fields)
      
def edit_image(request, uuid):
    return edit_instance(request, Image, uuid, image_required_fields, image_allowed_fields)
  
def delete_image(request, uuid):
    return delete_instance(request, Image, "slug", uuid)
def delete_image_by_id(request, id):
    return delete_instance(request, Image, "id", id)

#  --- --- --- --- --- --- #
# - - PROJECT <-> TAG  - - #
# --- --- --- --- --- ---  #

def add_tag_to_project(request, project_slug):
    return add_child_to(request, Project, Tag, "slug", project_slug)
  
def remove_tag_from_project(request, project_slug):
    return remove_child_from(request, Project, Tag, "slug", project_slug)