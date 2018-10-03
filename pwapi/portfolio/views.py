from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from portfolio.models import Tag, Image, Project
from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance
from pwapi.helpers.related_instances import add_child_to, remove_child_from
from pwapi.helpers.general import unmodified

from people.views import check_api_key

import bleach

# General error message for invalid requests:
errorJSON = [{'Error': 'No data for that request.'}]


def index(request):
    return HttpResponse('<h1>Portfolio</h1><ul><li><a href="projects">Projects</a></li><li><a href="tags">Tags</a></li></ul>')

  
#  --- --- --- --- --- --- #
# - - - - PROJECTS - - - - #
# --- --- --- --- --- ---  #

def projects(request):
    
    return index_response(
        request=request,
        model=Project,
        order_by='-sort_date'
    )

def get_project(request, slug):
    return get_instance(
        request=request,
        model=Project,
        lookup_field='slug',
        lookup_value=slug
    )

def new_project(request):
    return new_instance(
        request=request,
        model=Project
    )
  
def edit_project(request, slug):
    return edit_instance(
        request=request,
        model=Project,
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

def tags(request):   
  
    return index_response(
        request=request,
        model=Tag,
        order_by='name'
    )
  
def get_tag(request, slug):
    return get_instance(
        request=request,
        model=Tag,
        lookup_field='slug',
        lookup_value=slug
    )
  
def new_tag(request):
    return new_instance(
        request=request,
        model=Tag
    )
      
def edit_tag(request, slug):
    return edit_instance(
        request=request,
        model=Tag,
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
    return index_response(
        request=request,
        model=Image,
        order_by='project'
    )
  
def get_image(request, uuid):
    return get_instance(
        request=request,
        model=Image,
        lookup_field='uuid',
        lookup_value=uuid
    )
  
def new_image(request):
    return new_instance(
        request=request,
        model=Image
    )
      
def edit_image(request, uuid):
    return edit_instance(
        request=request,
        model=Image,
        lookup_field='uuid',
        lookup_value=uuid
    )
  
def delete_image_by_slug(request, uuid):
    return delete_instance(
        request=request,
        model=Image,
        lookup_field='uuid',
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