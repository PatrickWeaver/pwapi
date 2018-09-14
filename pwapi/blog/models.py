from django.db import models
from django.utils import timezone
from pwapi.helpers.create_slug import create_slug

class Post(models.Model):
    title = models.CharField(max_length=1024, null=True)
    slug = models.CharField(max_length=1024, unique=True, blank=True)
    summary = models.TextField(null=True)
    body = models.TextField()
    post_date = models.DateTimeField(default=timezone.now, blank=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    draft = models.BooleanField(default=False, blank=True)
    
    hide_if = "draft"

    def save(self, *args, **kwargs):
        slug_text = self.body
        if (self.title):
          slug_text = self.title    
        self.slug = create_slug(slug_text, self.slug, Post, self.id)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return u'{%s: %s}' % (self.title, self.body)
