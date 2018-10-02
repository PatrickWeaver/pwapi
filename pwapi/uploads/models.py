from django.db import models
import os
from uuid import uuid4
#from io import BytesIO
#from django.core.files.uploadedfile import InMemoryUploadedFile

def upload_file(instance, filename):
    return instance.uuid


class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=1024, unique=True, blank=True)
    upload = models.FileField(upload_to=upload_file)
    url = models.CharField(max_length=2048, unique=True, default="")
    
    index_fields = ['uploaded_at', 'filename', 'uuid', 'upload', 'url']
    required_fields = []
    allowed_fields = index_fields
    
    api_path = '/v1/uploads/'
    api_identifier = 'uuid'
    def get_api_url(self, request):
      #return request.scheme + "://" + request.get_host() + self.api_path + getattr(self, self.api_identifier, '')
      return ''
    
    def save(self, *args, **kwargs):
        new_uuid = str(uuid4())
        self.uuid = new_uuid
        self.url= "https://" + os.environ.get('AWS_STORAGE_BUCKET_NAME') + ".s3.amazonaws.com/" + "uploads" + "/" + new_uuid
        super(Upload, self).save(*args, **kwargs)
