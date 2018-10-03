from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from blobs.models import Blob
from people.views import check_api_key
from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance

import json

# General error message for invalid requests:
errorJSON = [{'Error': 'No data for that request.'}]

def blobs(request):
    return index_response(
        request=request,
        model=Blob,
        order_by='-created_date'
    )

def get_blob(request, slug):
    return get_instance(
        request=request,
        model=Blob,
        lookup_field='slug',
        lookup_value=slug
    )

def new_blob(request):
    return new_instance(
        request=request,
        model=Blob
    )

def edit_blob(request, slug):
    return edit_instance(
        requst=request,
        model=Blob,
        lookup_field='slug',
        lookup_value=slug
    )

def delete_blob_by_slug(request, slug):
    return delete_instance(
        request=request,
        model=Blob,
        lookup_field='slug',
        lookup_value=slug
    )

def delete_blob_by_id(request, id):
    return delete_instance(
        request=request,
        model=Blob,
        lookup_field='id',
        lookup_value=id
    )