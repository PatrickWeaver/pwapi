from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from portfolio.models import Tag, Image, Project
from pwapi.helpers.crud_instance import index_response, crud_response

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
    index_fields = ['name', 'slug', 'description', 'start_date', 'end_date', 'sort_date', 'project_url', 'status_id'] # Add: cover_photo_id
    order_by = '-sort_date'
    return index_response(request, Project, index_fields, order_by)
    
def project(request, slug):
    required_fields = ['name']
    allowed_fields = ['slug', 'description', 'start_date', 'end_date', 'sort_date', 'project_url', 'source_url', 'status_id'] + required_fields  
    return crud_response(request, Project, slug, required_fields, allowed_fields)

  

#  --- --- --- --- --- --- #
# - - - - - TAGS - - - - - #
# --- --- --- --- --- ---  #

def tags(request):   
    index_fields = ['name', 'slug', 'color', 'status', 'created_date']
    order_by = 'name'
    return index_response(request, Tag, index_fields, order_by)

  
def tag(request, slug):
    required_fields = ['name', 'color', 'slug']
    allowed_fields = ['status'] + required_fields 
    return crud_response(request, Tag, slug, required_fields, allowed_fields)
      
    


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