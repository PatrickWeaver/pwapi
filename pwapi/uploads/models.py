from django.db import models
#from io import BytesIO
#from django.core.files.uploadedfile import InMemoryUploadedFile

class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.TextField(default="")
    uuid = models.TextField(default="")
    upload = models.FileField()
