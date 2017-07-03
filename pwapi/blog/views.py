from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from blog.models import Post
import json

def posts(request):
    posts = Post.objects.all().values("post_title", "post_body", "post_date")
    posts_list = list(posts)
    return JsonResponse(posts_list, safe=False)
