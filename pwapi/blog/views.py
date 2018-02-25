from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from blog.models import Post
# In case the datetime module is needed it is imported as 'dt'
# https://docs.python.org/3/library/datetime.html
import datetime as dt
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

# posts function is at r'^blog/posts'
# This function returns all of the posts in the API.
# At some point this might require pagination
def posts(request):
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

def post(request):
    slug = bleach.clean(request.GET.get("slug", ""))
    try:
        post = Post.objects.filter(slug=slug)[0]
        post_dict = {}
        post_dict["slug"] = getattr(post, "slug")
        post_dict["title"] = getattr(post, "title")
        post_dict["summary"] = getattr(post, "summary")
        post_dict["body"] = getattr(post, "body")
        post_dict["post_date"] = getattr(post, "post_date")
        post_dict = expand_post(post_dict)
        response = {
            "posts_list": [post_dict]
        }
        return JsonResponse(response, safe=False)
    except Post.DoesNotExist:
        print("No post!")
        return JsonResponse(errorJSON, safe=False)


def new_post(request):
    # Start by assming there won't be a error with the request.
    error = False
    # Only accept POST requests, otherwise send an error
    if request.method == "POST":
        # Only accept requests with a body, other values like title and post_date can be blank and have defaults set.
        if request.body:
            jsonData = json.loads(request.body)
            if jsonData["body"]:
                # Might be better to set these defaults for title and post_date in the model?
                title = ""
                slug = ""
                summary = ""
                if jsonData["title"]:
                    title = bleach.clean(jsonData["title"])
                if jsonData["slug"]:
                    slug = bleach.clean(jsonData["slug"])
                if jsonData["summary"]:
                    summary = bleach.clean(jsonData["summary"])
                body = bleach.clean(jsonData["body"])

                #🚸 Find a way to check if it's a date.
                post_date = datetime.now()
                if jsonData["post_date"] and len(jsonData["post_date"]) > 2:
                    post_date = bleach.clean(jsonData["post_date"])
                post = Post(
                    title = title,
                    slug = slug,
                    summary = summary,
                    body = body,
                    post_date = post_date
                )
                post.save()
                post_list = [{
                    "success": True,
                    "title": title,
                    "slug": slug,
                    "summary": summary,
                    "body": body,
                    "post_date": post_date
                }]
                return JsonResponse(post_list, safe=False)

            else:
                return JsonResponse("Error: No Body", status=400, safe=False)
        else:
            error = True
            errorJSON = {"Error": "No Data"}
    else:
        instructions = {
          0: "New post must be submitted as POST request.",
          1: {
            "Required Fields:": {
              0: "title: max_length=1024",
              1: "body"
            },
            "Optional Fields": {
              0: "post_date"
            }
          }

        }

        return JsonResponse(instructions, safe=False)
        #error = True
    if error == True:
        return JsonResponse(errorJSON, safe=False)

def get_plaintext(markdown_text):
    return bleach.clean(''.join(BeautifulSoup(markdown_text).findAll(text=True)))

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
