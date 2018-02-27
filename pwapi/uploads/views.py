from django.shortcuts import render

from storages.backends.s3boto3 import S3Boto3Storage


from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Upload

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
