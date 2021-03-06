import sys, os

from uuid import uuid4

from django.db import models, transaction
from django.db.models import F, Max
from django.utils import timezone

from pwapi.helpers.create_slug import create_slug

# - - - - - - - - - - - - - -
# - - - - Tag - - - - - - - - 
# - - - - - - - - - - - - - -

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=256, null=True, blank=True)
    slug = models.CharField(max_length=1024, unique=True, blank=True)
    status = models.BooleanField(default=False, blank=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    
    index_fields = ['name', 'slug', 'color', 'status', 'created_date', 'id']
    required_fields = ['name']
    allowed_fields = ['status', 'slug', 'color', 'id'] + required_fields
    
    api_path = '/v1/portfolio/tags/'
    api_identifier = 'slug'
    def get_api_url(self, request):
        return request.scheme + "://" + request.get_host() + self.api_path + getattr(self, self.api_identifier, '')

    allowed_filters = [
        "status"
    ]

    def save(self, *args, **kwargs):
        if not self.status:
            self.color = None
            self.name = self.name.lower()   
        self.slug = create_slug(Tag, self.id, self.slug, self.name)
        super(Tag, self).save(*args, **kwargs)

        
        
# - - - - - - - - - - - - - -
# - - - Project - - - - - - - 
# - - - - - - - - - - - - - -
      
class Project(models.Model):
    name = models.CharField(max_length=1024)
    slug = models.CharField(max_length=1024, unique=True, blank=True)
    short_description = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(default='', blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sort_date = models.DateTimeField(blank=True)
    status = models.ForeignKey(Tag, related_name='project_status', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name='project_tags')
    project_url = models.CharField(max_length=1024, blank=True, null=True)
    source_url = models.CharField(max_length=1024, blank=True, null=True)
    is_hidden = models.BooleanField(default=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    
    index_fields = [
        'name',
        'slug',
        'short_description',
        'description',
        'start_date',
        'end_date',
        'sort_date',
        'project_url',
        'source_url',
        'is_hidden',
        'id'
      
    ]
    # Add: cover_photo_id

    required_fields = [
        'name',
        'status_id'
    ]
    allowed_fields = [
        'slug',
        'short_description',
        'description',
        'start_date',
        'end_date',
        'sort_date',
        'project_url',
        'source_url',
        'is_hidden',
        'id'
    ] + required_fields
    
    related_fields = [
        {
            'field_name': 'tags',
            'key_name': 'tags',
            'sort': 'name'
        },
        {
            'field_name': 'status',
            'key_name': 'status',
            'sort': 'name'
        },
        {
            'field_name': 'image_set',
            'key_name': 'images',
            'sort': 'order'
        }
    ]
    
    hide_if = 'is_hidden'
    
    allowed_filters = []

    api_path = '/v1/portfolio/projects/'
    api_identifier = 'slug'
    def get_api_url(self, request):
        return request.scheme + "://" + request.get_host() + self.api_path + getattr(self, self.api_identifier, '')

    def save(self, *args, **kwargs):
        self.slug = create_slug(Project, self.id, self.slug, self.name)
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

# - - - - - - - - - - - - - -
# - - - - - Image - - - - - -
# - - - - - - - - - - - - - -
def upload_file(instance, filename):
    return instance.uuid
  
  
def move_images(project, open_spot, move_until_spot, non_moving_pk):
    qs = Image.objects.get_queryset()
        
    with transaction.atomic():
        if move_until_spot > open_spot:
            qs.filter(
                project = project,
                order__lt = move_until_spot,
                order__gte = open_spot,
            ).exclude(
                pk = non_moving_pk,
            ).update(
                order = F('order') + 1,
            )
        else:
            qs.filter(
                project = project,
                order__lte = open_spot,
                order__gt = move_until_spot,
            ).exclude(
                pk = non_moving_pk,
            ).update(
                order = F('order') - 1,
            )
    
class Image(models.Model):
    uuid = models.UUIDField(default=uuid4, max_length=1024, unique=True, blank=True)
    order = models.IntegerField(blank=True)
    cover = models.BooleanField(default=False, blank=True)
    alt_text = models.CharField(max_length=1024, blank=True, null=True)
    caption = models.CharField(max_length=1024, blank=True, null=True)
    url = models.CharField(max_length=1024)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False, blank=False)
    

    index_fields = ['url', 'caption', 'cover', 'alt_text', 'uuid', 'created_date', 'project', 'project_id']
    required_fields = ['url', 'project_id']
    allowed_fields = ['caption', 'cover', 'alt_text', 'uuid', 'order'] + required_fields
    
    hide_if = 'is_hidden'

    allowed_filters = []
    
    def get_api_url(self, request):
      #return request.scheme + "://" + request.get_host() + self.api_path + getattr(self, self.api_identifier, '')
        return ''
    
      
    def save(self, *args, **kwargs):
        # Getting Blank URLS:
        # This isn't working right now
        if self.url == "  " or self.url == " ":
          PRINT("HELLO!!!!")
          self.url = None
      
        # Reorder
        number_of_images = Image.objects.filter(
            project = self.project,
        ).aggregate(
            Max('order')
        )['order__max']
        
        if number_of_images is None:
            number_of_images = 0
        
        max_order = number_of_images + 1
        
        
        self.order = int(self.order)
        if self.order == 0:
          self.order = 1
        elif not self.order or self.order < 1 or self.order > max_order:
            self.order = max_order
            
        try:
            obj = Image.objects.filter(project=self.project, uuid=self.uuid).get()
            move_images(obj.project, self.order, obj.order, obj.pk)

        except Exception as e:
            print("*#*#*#*#*#*#*#*#*#*#*#*#*")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("*#*#*#*#*#*#*#*#*#*#*#*#*")

            move_images(self.project, self.order, number_of_images, None)
            
        if self.cover:
            try:
                cover_image = Image.objects.filter(project=self.project, cover=True).get()
                if cover_image != self:
                    cover_image.cover = False
                    cover_image.save()
                
            except:
                pass
        
        super(Image, self).save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        try:
            project_images = Image.objects.filter(project=self.project).order_by('order')[self.order + 1:]
            for i in project_images:
                i.order -= 1
                i.save()
        except:
            pass
        
        super(Image, self).delete(*args, **kwargs)