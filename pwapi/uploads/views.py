from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from storages.backends.s3boto3 import S3Boto3Storage


from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from . models import Upload

def root(request):
    response = {}
    return JsonResponse(response, safe=False)

def new(request):
    print(request.method + ": " + request.path);
    if request.method == "GET":
        response = [{"Error": "File upload only via POST."}]
        return JsonResponse(response, safe=False)
    elif request.method == "POST":
        return upload_file(request)

def upload_file(request):
    file_dict = {
        "upload": request.FILES["file"],
        "filename": request.POST["filename"],
        "uuid": request.POST["uuid"]
    }

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
