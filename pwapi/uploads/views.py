from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from storages.backends.s3boto3 import S3Boto3Storage

from pwapi.helpers.crud_instance import index_response, get_instance, new_instance, edit_instance, delete_instance

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from . models import Upload

def root(request):
    return index_response(
        request=request,
        model=Upload,
        order_by='-uploaded_at'
    )

def new(request):
    print(request.method + ": " + request.path);
    if request.method == "GET":
        response = [{"Error": "File upload only via POST."}]
        return JsonResponse(response, safe=False)
    elif request.method == "POST":
        return upload_file(request)

def upload_file(request):
    file_dict = {
        "upload": request.FILES["file"]
    }
    
    print("**")
    print(file_dict["upload"])

    upload = Upload(**file_dict)
    upload.save()

    upload_url = upload.upload.url
    response = [{"Status": "Upload complete.", "upload_url": upload_url}]
    return JsonResponse(response, safe=False)


class UploadStorage(S3Boto3Storage):
    location = 'uploads'
    file_overwrite = False


class UploadCreateView(CreateView):
    model = Upload
    fields = ['upload', ]
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uploads = Upload.objects.all()
        context['uploads'] = uploads
        return context
