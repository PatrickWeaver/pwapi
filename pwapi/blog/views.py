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

# General error message for invalid requests:
errorJSON = [{"Error": "No data for that request."}]

# posts function is at r'^blog/posts'
# This function returns all of the posts in the API.
# At some point this might require pagination
def posts(request):
    # 🚸 Need to make sure incorrect parameters don't crash api server
    # This is for pagination on the blog, should try to make this more general so I can use it elsewhere.
    page = int(bleach.clean(request.GET.get("page", 1)))
    if type(page) != int:
        page = 1
    end_page = page * 5
    start_page = end_page - 5
    all_posts = Post.objects.all()
    number_of_posts = all_posts.count();
    posts = all_posts.order_by("-post_date")[start_page:end_page].values("post_title", "post_body", "post_date")
    posts_list = list(posts)
    posts_response = {
        "total_posts": number_of_posts,
        "page": page,
        "posts_list": posts_list,
    }
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(posts_response, safe=False)

def new_post(request):
    # Start by assming there won't be a error with the request.
    error = False
    # Only accept POST requests, otherwise send an error
    if request.method == "POST":
        # Only accept requests with a post_body, other values like post_title and post_date can be blank and have defaults set.
        if request.POST.get("post_body"):
            # Might be better to set these defaults for post_title and post_date in the model?
            post_title = bleach.clean(request.POST.get("post_title", ""))
            post_body = bleach.clean(request.POST["post_body"])
            #🚸 Find a way to check if it's a date.

            post_date = bleach.clean(request.POST.get("post_date", datetime.now()))
            if len(post_date) < 2:
                post_date = datetime.now()
            # Might also want to set this as default in the model
            created_date = datetime.now()
            post = Post(post_title = post_title, post_body = post_body, post_date = post_date, created_date = created_date)
            post.save()
            post_list = [{
                "post_title": post_title,
                "post_body": post_body,
                "post_date": post_date,
                "created_date": created_date
            }]
            return JsonResponse(post_list, safe=False)

        else:
            return JsonResponse("NO POST_BODY", safe=False)
    else:
        return JsonResponse(("NOT POST, was: " + request.method), safe=False)
        #error = True
    if error == True:
        return JsonResponse(errorJSON, safe=False)
