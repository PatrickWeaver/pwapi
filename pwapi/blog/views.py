from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from blog.models import Post
from people.views import check_api_key
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
    index_fields = [
      'title',
      'slug',
      'summary',
      'post_date',
      'body',
      'draft'
    ]
    return index_response(
        request=request,
        model=Post,
        index_fields=index_fields,
        order_by='-post_date',
        modify_each_with=expand_preview_post,
        instance_path_field='slug'
    );
  
post_required_fields = ['body']
post_allowed_fields = [
    'slug',
    'title',
    'summary',
    'post_date',
    'draft',
    'id'
] + post_required_fields

def get_post(request, slug):
    return get_instance(
        request=request,
        model=Post,
        allowed_fields=post_allowed_fields,
        lookup_field='slug',
        lookup_value=slug,
        instance_path_field='slug'
    )
  
def new_post(request):
    return new_instance(
        request=request,
        model=Post,
        required_fields=post_required_fields,
        allowed_fields=post_allowed_fields
    )
  
def edit_post(request, slug):
    return edit_instance(
        request=request,
        model=Post,
        required_fields=post_required_fields,
        allowed_fields=post_allowed_fields,
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


def expand_preview_post(post_dict):
    plaintext_body = post_dict['body']['plaintext']
    full_post = False
    if len(plaintext_body) <= 280:
        full_post = True
    post_dict['full_post_in_preview'] = full_post
    post_dict['post_preview'] = plaintext_body[0:279] + (' . . .' if not full_post else '')
    del post_dict['body']
    return post_dict
