from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from blog.models import Post
from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance

from datetime import datetime
# https://docs.python.org/3/library/json.html
import json

# General error message for invalid requests:
errorJSON = [{'Error': 'No data for that request.'}]

# This function returns all of the posts in the API.
# At some point this might require pagination
def index(request):
    response = {
        'all_posts' : '/v1/blog/posts/'
    }

    return JsonResponse(response, safe=False) 

def posts(request):

    return index_response(
        request=request,
        model=Post,
        order_by='-post_date'
    )

def get_post(request, slug):
    return get_instance(
        request=request,
        model=Post,
        lookup_field='slug',
        lookup_value=slug
    )
  
def new_post(request):
    return new_instance(
        request=request,
        model=Post
    )
  
def edit_post(request, slug):
    return edit_instance(
        request=request,
        model=Post,
        lookup_field='slug',
        lookup_value=slug
    )
  
def delete_post_by_slug(request, slug):
    return delete_instance(
        request=request,
        model=Post,
        lookup_field='slug',
        lookup_value=slug
    )
  
def delete_post_by_id(request, id):
    return delete_instance(
        request=request,
        model=Post,
        lookup_field='id',
        lookup_value=id
    )
