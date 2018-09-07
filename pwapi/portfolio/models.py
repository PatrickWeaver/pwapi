import uuid

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
        super(Tag, self).save(*args, **kwargs)

class Image(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=0)
    cover = models.BooleanField(default=False)
    caption = models.CharField(max_length=1024, null=True)
    url = models.CharField(max_length=1024)
    created_date = models.DateTimeField(default=datetime.now)

class Project(models.Model):
    name = models.CharField(max_length=1024, default="")
    slug = models.CharField(max_length=1024, unique=True)
    description = models.TextField(default="")
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sort_date = models.DateTimeField()
    status = models.ForeignKey(Tag, related_name="project_status", on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name="project_tags")
    project_url = models.CharField(max_length=1024, blank=True, null=True)
    source_url = models.CharField(max_length=1024, blank=True, null=True)
    images = models.ManyToManyField(Image)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=datetime.now)


    def save(self, *args, **kwargs):
        self.slug = create_slug(self.name, self.slug, self.end_date)
        self.sort_date = get_sort_date(self.end_date, self.start_date)
        super(Project, self).save(*args, **kwargs)
        
def get_sort_date(end_date, start_date):
    if end_date:
        print('using end date')
        return end_date
    elif start_date:
        print('using start date')
        return start_date
    else:
        print('using now')
        return datetime.now()
