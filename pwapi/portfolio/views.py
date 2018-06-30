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
# Allow iframe tags and attributes for YouTube videos:
bleach.sanitizer.ALLOWED_TAGS.append(u"iframe")
bleach.sanitizer.ALLOWED_ATTRIBUTES[u"iframe"] = [u"width", u"height", u"src", u"frameborder", u"allow", u"allowfullscreen"]

# General error message for invalid requests:
errorJSON = [{"Error": "No data for that request."}]

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
    elif request.method == "POST":
        return new_project(request, slug)
    elif request.method == "PUT":
        return edit_project(request, slug)
    elif request.method == "DELETE":
        return delete_project(request, slug)

def get_project(request, slug):
    print("get_project " + slug)
    project = find_project_from_slug(slug)
    project_dict = project_dict_from_project(project)
    if project_dict == {}:
        return JsonResponse(errorJSON, safe=False)
    else:
        response = project_dict
        return JsonResponse(response, safe=False)

def new_project(request, slug):
    print("new_project " + slug)
    project_dict = project_dict_from_request(request)
    project = project_from_project_dict(project_dict)
    project_response = response_from_project(project)
    if not project_response:
        return JsonResponse(errorJSON, safe=False)
    return JsonResponse(project_response, safe=False)


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

def project_dict_from_request(request):
    if not request.body:
        return False
    jsonData = json.loads(request.body)
    if "name" not in jsonData:
        return False
    if "api_key" not in jsonData:
        return False
    #api_key_valid = check_api_key(bleach.clean(jsonData["api_key"]))
    api_key_valid = True
    if not api_key_valid:
        return False
    # Might be better to set these defaults for title and post_date in the model?
    name = ""
    slug = ""
    description = ""
    start_date = None
    end_date = None
    project_url = ""
    source_url = ""
    status_id = False
    if "name" in jsonData:
        name = bleach.clean(jsonData["name"])
    if "slug" in jsonData:
        slug = bleach.clean(jsonData["slug"])
    if "description" in jsonData:
        description = bleach.clean(jsonData["description"])
    if "project_url" in jsonData:
        project_url = bleach.clean(jsonData["project_url"])
    if "source_url" in jsonData:
        source_url = bleach.clean(jsonData["source_url"])
    if "status_id" in jsonData:
        status_id = bleach.clean(jsonData["status_id"])

    #🚸 Find a way to check if it's a date.
    start_date = datetime.now()
    if "start_date" in jsonData and len(jsonData["start_date"]) > 2:
        start_date = bleach.clean(jsonData["start_date"])
    end_date = datetime.now()
    if "end_date" in jsonData and len(jsonData["end_date"]) > 2:
        end_date = bleach.clean(jsonData["end_date"])
    project_dict = {
        "name":         name,
        "slug":         slug,
        "description":  description,
        "start_date":   start_date,
        "end_date":     end_date,
        "project_url":  project_url,
        "source_url":   source_url,
        "status_id":    status_id
    }
    return project_dict

def project_from_project_dict(project_dict):
    if not project_dict:
        return False
    project = Project(**project_dict)
    project.save()
    return project

def response_from_project(project):
    response = {
        "success": True,
        "name": project.name,
        "slug": project.slug,
        "description": project.description,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "project_url": project.project_url,
        "source_url": project.source_url,
        "status_id": project.status_id
    }
    return response

def edit_project(request, slug):
    print("edit_project " + slug)
    project = find_project_from_slug(slug)
    project_dict = project_dict_from_request(request)
    print(project_dict)
    if not project_dict:
        return JsonResponse(errorJSON, safe=False)
    project = update_project_from_dict(project, project_dict)
    project.save()
    project_response = response_from_project(project)
    if not project_response:
        return JsonResponse(errorJSON, safe=False)
    return JsonResponse(project_response, safe=False)

def find_project_from_slug(slug):
    try:
        project = Project.objects.filter(slug=slug)[0]
        return project
    except Project.DoesNotExist:
        return False

def update_project_from_dict(project, project_dict):
    for key, value in project_dict.items():
        if hasattr(project, key):
            setattr(project, key, value)
        else:
            return False
    return project

def delete_project(request, slug):
    project = find_project_from_slug(slug)
    project.delete()
    return JsonResponse({"success": True})
