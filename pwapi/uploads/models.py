from django.db import models
import os
from uuid import uuid4
#from io import BytesIO
#from django.core.files.uploadedfile import InMemoryUploadedFile

def upload_file(instance, filename):
    return instance.uuid


class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=1024, unique=True, default="", blank=True)
    upload = models.FileField(upload_to=upload_file)
    url = models.CharField(max_length=2048, unique=True, default="")
    
    index_fields = ['uploaded_at', 'filename', 'uuid', 'upload', 'url']
    required_fields = []
    allowed_fields = index_fields
    
    def save(self, *args, **kwargs):
        uuid = str(uuid4())
        self.uuid = uuid
        self.url= "https://" + os.environ.get('AWS_STORAGE_BUCKET_NAME') + ".s3.amazonaws.com/" + "uploads" + "/" + uuid
        super(Upload, self).save(*args, **kwargs)
