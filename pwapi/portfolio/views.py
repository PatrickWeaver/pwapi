from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from portfolio.models import Tag, Image, Project
from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance
from pwapi.helpers.related_instances import add_child_to, remove_child_from
from pwapi.helpers.general import unmodified

from people.views import check_api_key

# https://docs.python.org/3/library/json.html
import json
import bleach

# General error message for invalid requests:
errorJSON = [{'Error': 'No data for that request.'}]

project_related_fields = [
    {
        'field_name': 'tags',
        'related_name': 'project_tags'
    },
    {
        'field_name': 'status',
        'relateed_name': 'project_status'
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
    
    return index_response(
        request=request,
        model=Project,
        index_fields=index_fields,
        order_by='-sort_date',
        related_fields=project_related_fields,
        instance_path_field='slug',
        sort_field='sort_date'
    )

  
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
    'id'
] + project_required_fields # project_related_fields also added later

def get_project(request, slug):
    return get_instance(
        request=request,
        model=Project,
        allowed_fields=project_allowed_fields,
        lookup_field='slug',
        lookup_value=slug,
        related_fields=project_related_fields,
        instance_path_field='slug'
    )

def new_project(request):
    return new_instance(
        request=request,
        model=Project,
        required_fields=project_required_fields,
        allowed_fields=project_allowed_fields
    )
  
def edit_project(request, slug):
    return edit_instance(
        request=request,
        model=Project,
        required_fields=project_required_fields,
        allowed_fields=project_allowed_fields,
        lookup_field='slug',
        lookup_value=slug
    )
  
def delete_project_by_slug(request, slug):
    return delete_instance(
        request=request,
        model=Project,
        lookup_field='slug',
        lookup_value=slug
    )
  
def delete_project_by_id(request, id):
    return delete_instance(
        request=request,
        model=Project,
        lookup_field='id',
        lookup_value=id
    )
    

#  --- --- --- --- --- --- #
# - - - - - TAGS - - - - - #
# --- --- --- --- --- ---  #

def modify_new_tags(request_dict):
    try:
        status = request_dict['status']
    except:
        status = False
    if not status:
        request_dict['color'] = None
        request_dict['name'] = request_dict['name'].lower()
    return request_dict

def tags(request):   
    index_fields = ['name', 'slug', 'color', 'status', 'created_date', 'id']
    return index_response(
        request=request,
        model=Tag,
        index_fields=index_fields,
        order_by='name',
        instance_path_field="slug"
    )

tag_required_fields = ['name']
tag_allowed_fields = ['status', 'slug', 'color'] + tag_required_fields
  
def get_tag(request, slug):
    return get_instance(
        request=request,
        model=Tag,
        allowed_fields=tag_allowed_fields,
        lookup_field='slug',
        lookup_value=slug,
        instance_path_field="slug"
    )
  
def new_tag(request):
    return new_instance(
        request=request,
        model=Tag,
        required_fields=tag_required_fields,
        allowed_fields=tag_allowed_fields,
        modify_with=modify_new_tags
    )
      
def edit_tag(request, slug):
    return edit_instance(
        request=request,
        model=Tag,
        required_fields=tag_required_fields,
        allowed_fields=tag_allowed_fields,
        lookup_field='slug',
        lookup_value=slug
    )
  
def delete_tag_by_slug(request, slug):
    return delete_instance(
        request=request,
        model=Tag,
        lookup_field='slug',
        lookup_value=slug
    )
  
def delete_tag_by_id(request, id):
    return delete_instance(
        request=request,
        model=Tag,
        lookup_field='id',
        lookup_value=id
    )


#  --- --- --- --- --- --- #
# - - - - IMAGES - - - - - #
# --- --- --- --- --- ---  #

def images(request):
    index_fields = ['url', 'caption', 'cover', 'uuid', 'created_date', 'project']
    return index_response(
        request=request,
        model=Image,
        index_fields=index_fields,
        order_by='project'
    )

image_required_fields = ['url', 'project']
image_allowed_fields = ['caption', 'cover'] + image_required_fields
  
def get_image(request, uuid):
    return get_instance(
        request=request,
        model=Image,
        allowed_fields=image_allowed_fields,
        lookup_field='uuid',
        lookup_value=uuid
    )
  
def new_image(request):
    return new_instance(
        request=request,
        model=Image,
        required_fields=image_required_fields,
        allowed_fields=image_allowed_fields
    )
      
def edit_image(request, uuid):
    return edit_instance(
        request=request,
        model=Image,
        required_fields=image_required_fields,
        allowed_fields=image_allowed_fields,
        lookup_field='uuid',
        lookup_value=uuid
    )
  
def delete_image_by_slug(request, uuid):
    return delete_instance(
        request=request,
        model=Image,
        lookup_field='slug',
        lookup_value=uuid
    )

def delete_image_by_id(request, id):
    return delete_instance(
        request=request,
        model=Image,
        lookup_field='id',
        lookup_value=id
    )

#  --- --- --- --- --- --- #
# - - PROJECT <-> TAG  - - #
# --- --- --- --- --- ---  #

def add_tag_to_project(request, project_slug):
    return add_child_to(
        request=request,
        parent_model=Project,
        child_model=Tag,
        parent_key='slug',
        parent_identifier_value=project_slug,
        child_field_name_on_parent='tags'
    )
  
def remove_tag_from_project(request, project_slug):
    return remove_child_from(
        request=request,
        parent_model=Project,
        child_model=Tag, 
        parent_key='slug',
        parent_identifier_value=project_slug,
        child_field_name_on_parent='tags'
    )