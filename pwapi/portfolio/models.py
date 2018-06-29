from django.db import models
from datetime import datetime
from pwapi.helpers.create_slug import create_slug

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=6)
    slug = models.CharField(max_length=50, unique=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.slug = create_slug(self.name, self.slug, self.created_date)
        super(Post, self).save(*args, **kwargs)

class Image(models.Model):
    order = models.IntegerField(default=0)
    cover = models.BooleanField(default=False)
    caption = models.CharField(max_length=1024)
    url = models.CharField(max_length=1024)

class Project(models.Model):
    name = models.CharField(max_length=1024, default="")
    slug = models.CharField(max_length=1024, unique=True)
    description = models.TextField(default="")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.ForeignKey(Tag, related_name="project_status", on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name="project_tags")
    project_url = models.CharField(max_length=1024)
    source_url = models.CharField(max_length=1024)
    images = models.ManyToManyField(Image)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=datetime.now)


    def save(self, *args, **kwargs):
        self.slug = create_slug(self.name, self.slug, self.end_date)
        super(Post, self).save(*args, **kwargs)
