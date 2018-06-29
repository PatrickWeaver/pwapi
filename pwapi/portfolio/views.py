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

def project(request, slug):
    print(request.method + ": " + request.path);
    if request.method == "GET":
        return get_project(request, slug)
    #elif request.method == "POST":
    #    return new_project(request, slug)
    #elif request.method == "PUT":
    #    return edit_project(request, slug)
    #elif request.method == "DELETE":
    #    return delete_project(request, slug)

def get_project(request, slug):
    print("get_project " + slug)
    project = find_project_from_slug(slug)
    project_dict = project_dict_from_project(project)
    if project_dict == {}:
        return JsonResponse(errorJSON, safe=False)
    else:
        response = project_dict
        return JsonResponse(response, safe=False)


def find_project_from_slug(slug):
    try:
        project = Project.objects.filter(slug=slug)[0]
        return project
    except Project.DoesNotExist:
        return False

def project_dict_from_project(project):
    project_dict = {}
    project_dict["name"] = getattr(project, "name")
    project_dict["slug"] = getattr(project, "slug")
    project_dict["description"] = getattr(project, "description")
    project_dict["start_date"] = getattr(project, "start_date")
    project_dict["end_date"] = getattr(project, "end_date")
    project_dict["project_url"] = getattr(project, "project_url")
    project_dict["source_url"] = getattr(project, "source_url")
    project_dict["status_id"] = getattr(project, "status_id")
    project_dict = expand_project(project_dict)
    return project_dict


def expand_project(project):
    #html_body = markdown(project["description"], extensions=["markdown.extensions.extra"])
    #post["html_body"] = html_body
    #plaintext_body = get_plaintext(html_body)
    #post["plaintext_body"] = plaintext_body
    return project
