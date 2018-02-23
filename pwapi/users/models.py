from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    api_key = models.CharField(max_length=255)
