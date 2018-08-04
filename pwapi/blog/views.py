from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from blog.models import Post
from people.views import check_api_key

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
        "all_posts" : "http://localhost:8000/v1/blog/posts/"
    }

    return JsonResponse(response, safe=False)


def posts(request):
    response = {"ok": "ok"}
    # 🚸 Need to make sure incorrect parameters don't crash api server
    # This is for pagination on the blog, should try to make this more general so I can use it elsewhere.
    page = int(bleach.clean(request.GET.get("page", "1")))
    quantity = int(bleach.clean(request.GET.get("quantity", "5")))
    if type(page) != int:
        page = 1
    end_of_page = page * quantity
    start_of_page = end_of_page - quantity
    all_posts = Post.objects.all()
    number_of_posts = all_posts.count();
    posts = all_posts.order_by("-post_date")[start_of_page:end_of_page].values("title", "slug", "summary", "body", "post_date")
    index_posts_list = []
    for post in posts:
        index_post = {
            "title":        post["title"],
            "slug":         post["slug"],
            "summary":      post["summary"],
            "post_date":    post["post_date"]
        }
        index_post = {**index_post, **preview_post(post)}
        index_posts_list.append(index_post)
    response = {
        "total_posts":  number_of_posts,
        "page":         page,
        "posts_list":   index_posts_list,
    }
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(response, safe=False)

def post(request, slug):
    print(request.method + ": " + request.path);
    if request.method == "GET":
        return get_post(request, slug)
    elif request.method == "POST":
        return new_post(request, slug)
    elif request.method == "PUT":
        return edit_post(request, slug)
    elif request.method == "DELETE":
        return delete_post(request, slug)

def get_post(request, slug):
    print("get_post " + slug)
    post = find_post_from_slug(slug)
    post_dict = post_dict_from_post(post)
    if post_dict == {}:
        return JsonResponse(errorJSON, safe=False)
    else:
        response = post_dict
        return JsonResponse(response, safe=False)

def new_post(request, slug):
    print("new_post " + slug)
    post_dict = post_dict_from_request(request)
    if post_dict:
        post = post_from_post_dict(post_dict)
        post_response = response_from_post(post)
        if post_response:
            return JsonResponse(post_response, safe=False)
    return JsonResponse(errorJSON, safe=False)
    
        

def edit_post(request, slug):
    print("edit_post " + slug)
    post = find_post_from_slug(slug)
    post_dict = post_dict_from_request(request)
    if post_dict:       
        post = update_post_from_dict(post, post_dict)
        post.save()
        post_response = response_from_post(post)
        if post_response:
            return JsonResponse(post_response, safe=False)
    return JsonResponse(errorJSON, safe=False)


def delete_post(request, slug):
    post = find_post_from_slug(slug)
    post.delete()
    return JsonResponse({"success": True})


def find_post_from_slug(slug):
    try:
        post = Post.objects.get(slug=slug)
        return post
    except Post.DoesNotExist:
        return False

def post_dict_from_post(post):
    post_dict = {}
    post_dict["slug"] = getattr(post, "slug")
    post_dict["title"] = getattr(post, "title")
    post_dict["summary"] = getattr(post, "summary")
    post_dict["body"] = getattr(post, "body")
    post_dict["post_date"] = getattr(post, "post_date")
    post_dict = expand_post(post_dict)
    return post_dict

def post_dict_from_request(request):
    if not request.body:
        return False
    jsonData = json.loads(request.body.decode('utf-8'))
    if "body" not in jsonData:
        # ***
        print("No Body")
        return False
    if "api_key" not in jsonData:
        # ***
        print("No API KEY")
        return False
    api_key_valid = check_api_key(bleach.clean(jsonData["api_key"]))
    if not api_key_valid:
        return False
    # Might be better to set these defaults for title and post_date in the model?
    title = ""
    slug = ""
    summary = ""
    if "title" in jsonData:
        title = bleach.clean(jsonData["title"])
    if "slug" in jsonData:
        slug = bleach.clean(jsonData["slug"])
    if "summary" in jsonData:
        summary = bleach.clean(jsonData["summary"])
    body = bleach.clean(jsonData["body"])

    #🚸 Find a way to check if it's a date.
    post_date = datetime.now()
    if "post_date" in jsonData and len(jsonData["post_date"]) > 2:
        post_date = bleach.clean(jsonData["post_date"])
    post_dict = {
        "title":      title,
        "slug":       slug,
        "summary":    summary,
        "body":       body,
        "post_date":  post_date
    }
    return post_dict

def post_from_post_dict(post_dict):
    if not post_dict:
        return False
    post = Post(**post_dict)
    post.save()
    return post

def response_from_post(post):
    response = {
        "success": True,
        "title": post.title,
        "slug": post.slug,
        "summary": post.summary,
        "body": post.body,
        "post_date": post.post_date
    }
    return response

def update_post_from_dict(post, post_dict):
    for key, value in post_dict.items():
        if hasattr(post, key):
            setattr(post, key, value)
        else:
            return False
    return post


def get_plaintext(markdown_text):
    return bleach.clean(''.join(BeautifulSoup(markdown_text, "html5lib").findAll(text=True)))

def expand_post(post):
    html_body = markdown(post["body"], extensions=["markdown.extensions.extra"])
    post["html_body"] = html_body
    plaintext_body = get_plaintext(html_body)
    post["plaintext_body"] = plaintext_body
    return post

def preview_post(post):
    html_body = markdown(post["body"], extensions=["markdown.extensions.extra"])
    plaintext_body = get_plaintext(html_body)
    full_post = False
    if len(plaintext_body) <= 280:
        full_post = True
    index_post = {
        "full_post_in_preview": full_post,
        "post_preview": plaintext_body[0:279] + (" . . ." if not full_post else "")
    }
    # Try to figure out how to get a markdown preview also
    return index_post
