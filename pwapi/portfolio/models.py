import uuid

from django.db import models
from django.utils import timezone

from pwapi.helpers.create_slug import create_slug

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=256, null=True, blank=True)
    slug = models.CharField(max_length=1024, unique=True, blank=True)
    status = models.BooleanField(default=False, blank=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.slug = create_slug(self.name, self.slug, Tag, self.id)
        super(Tag, self).save(*args, **kwargs)

class Project(models.Model):
    name = models.CharField(max_length=1024)
    slug = models.CharField(max_length=1024, unique=True, blank=True)
    description = models.TextField(default="", blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sort_date = models.DateTimeField(blank=True)
    status = models.ForeignKey(Tag, related_name="project_status", on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name="project_tags")
    project_url = models.CharField(max_length=1024, blank=True, null=True)
    source_url = models.CharField(max_length=1024, blank=True, null=True)
    is_hidden = models.BooleanField(default=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    hide_if = "is_hidden"

    def save(self, *args, **kwargs):
        self.slug = create_slug(self.name, self.slug, Project, self.id)
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
        return timezone.now()
      
class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True)
    order = models.IntegerField(default=0, blank=True, unique=True)
    cover = models.BooleanField(default=False, blank=True)
    caption = models.CharField(max_length=1024, null=True)
    url = models.CharField(max_length=1024)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    #def save(self, *args, **kwargs):
        #self.order = Image.objects.filter(project=self.project).count() 
