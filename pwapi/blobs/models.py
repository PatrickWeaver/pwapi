from django.db import models
from django.utils import timezone
from pwapi.helpers.create_slug import create_slug
from pwapi.helpers.general import get_plaintext


class Blob(models.Model):
    title = models.CharField(max_length=1024, null=True, blank=True)
    slug = models.CharField(max_length=1024, unique=True, blank=True)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    is_hidden = models.BooleanField(default=False, blank=True)

    index_fields = [
        'title',
        'slug',
        'body',
        'created_date',
        'is_hidden'
    ]

    required_fields = ['body']

    allowed_fields = [
        'title',
        'slug',
        'is_hidden',
        'id',
        'created_date'
    ] + required_fields

    hide_if = 'is_hidden'

    api_path = '/v1/blobs/'
    api_identifier = 'slug'

    def get_api_url(self, request):
      return request.scheme + "://" + request.get_host() + self.api_path + getattr(self, self.api_identifier, '')


    def save(self, *args, **kwargs):  
        self.slug = create_slug(Blob, self.slug, self.title)
        super(Blob, self).save(*args, **kwargs)

    def __str__(self):
        return u'{%s: %s}' % (self.title, self.slug)



'''

    def get_api_url(self, request):
      return request.scheme + "://" + request.get_host() + self.api_path + getattr(self, self.api_identifier, '')

    def save(self, *args, **kwargs):  
        self.slug = create_slug(Post, self.id, self.slug, self.title, self.body)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return u'{%s: %s}' % (self.title, self.body)
    
    def expand_post_preview(post_dict):
        html_body = post_dict['body']['html']
        plaintext_body = get_plaintext(html_body)
        full_post = False
        if len(plaintext_body) <= 280:
            full_post = True
        post_dict['full_post_in_preview'] = full_post
        post_dict['post_preview'] = plaintext_body[0:279] + (' . . .' if not full_post else '')
        del post_dict['body']
        return post_dict
    index_modify_with = expand_post_preview
'''