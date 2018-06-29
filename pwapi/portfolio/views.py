from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from portfolio.models import Tag, Image, Project
from people.views import check_api_key

from datetime import datetime
# https://docs.python.org/3/library/json.html
import json
# bleach is used to sanatize request input
# https://pypi.python.org/pypi/bleach
import bleach

def index(request):
    return HttpResponse("Portfolio")


def projects(request):
    response = {"ok": "ok"}
    # No pagination for now:
    # See blog.views.posts for example

    all_projects = Project.objects.all()
    number_of_projects = all_projects.count();
    projects = all_projects.order_by("-start_date").values("name", "slug", "description", "start_date", "end_date", "project_url", "status_id")
    index_list = []
    for project in projects:
        index_project = {
            "name":         project["name"],
            "slug":         project["slug"],
            "description":  project["description"],
            "start_date":   project["start_date"],
            "end_date":     project["end_date"],
            "project_url":  project["project_url"],
            "status_id":    project["status_id"]
        }
        index_list.append(index_project)
    response = {
        "total_projects":  number_of_projects,
        "projects_list":   index_list,
    }
    # on safe=False: https://stackoverflow.com/questions/28740338/creating-json-array-in-django
    return JsonResponse(response, safe=False)
