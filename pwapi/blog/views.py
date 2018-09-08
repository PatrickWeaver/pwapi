from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from blog.models import Post
from people.views import check_api_key
from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance

from datetime import datetime
# https://docs.python.org/3/library/json.html
import json
# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach
# Allow iframe tags and attributes for YouTube videos:
bleach.sanitizer.ALLOWED_TAGS.append(u"iframe")
bleach.sanitizer.ALLOWED_ATTRIBUTES[u"iframe"] = [u"width", u"height", u"src", u"frameborder", u"allow", u"allowfullscreen"]
# BeautifulSoup4 is used to get plaintext from HTML (via Markdown)
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
# Markdown is used to parse markdown to HTML to send to Beautiful Soup.
# https://pypi.python.org/pypi/Markdown
from markdown import markdown

# General error message for invalid requests:
errorJSON = [{"Error": "No data for that request."}]

# This function returns all of the posts in the API.
# At some point this might require pagination
def index(request):
    response = {
        "all_posts" : "/v1/blog/posts/"
    }

    return JsonResponse(response, safe=False)
  

def posts(request):
    #index_fields = ['title', 'slug', 'summary', 'post_date']
    index_fields = ['title', 'slug', 'summary', 'post_date', 'body']
    order_by = '-post_date'
    #return index_response(request, Post, index_fields, order_by);
    return_json = False
    index_dict = index_response(request, Post, index_fields, order_by, return_json)
    for post_dict in index_dict["post_list"]:
        post_dict = expand_preview_post(post_dict)
    return JsonResponse(index_dict)

  
post_required_fields = ['body']
post_allowed_fields = [
    'slug',
    'title',
    'summary',
    'post_date'
] + post_required_fields

def get_post(request, slug):
    # return get_instance(Post, slug, post_allowed_fields)
    return_json = False
    post_dict = get_instance(Post, slug, post_allowed_fields, return_json)
    expanded_post_dict = expand_post(post_dict)
    return JsonResponse(expanded_post_dict)
  
def new_post(request):
    return new_instance(request, Post, post_required_fields, post_allowed_fields)
  
def edit_post(request, slug):
    return edit_instance(request, Post, slug, post_required_fields, post_allowed_fields)
  
def delete_post(request, slug):
    return delete_instance(request, Post, slug)


def get_plaintext(markdown_text):
    return bleach.clean(''.join(BeautifulSoup(markdown_text, "html5lib").findAll(text=True)))

def expand_post(post_dict):
    html_body = markdown(post_dict["body"], extensions=["markdown.extensions.extra"])
    post_dict["html_body"] = html_body
    post_dict["plaintext_body"] = get_plaintext(html_body)
    return post

def expand_preview_post(post_dict):
    print(post_dict)
    html_body = markdown(post_dict["body"], extensions=["markdown.extensions.extra"])
    plaintext_body = get_plaintext(html_body)
    full_post = False
    if len(plaintext_body) <= 280:
        full_post = True
    post_dict["full_post_in_preview"] = full_post
    post_dict["post_preview"] = plaintext_body[0:279] + (" . . ." if not full_post else "")
    post_dict["body"] = None
    # Try to figure out how to get a markdown preview also
    return post_dict
