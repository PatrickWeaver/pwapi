from django.db import models
from datetime import datetime
from pwapi.helpers.create_slug import create_slug

class Post(models.Model):
    title = models.CharField(max_length=1024, default="")
    slug = models.CharField(max_length=1024, unique=True)
    summary = models.TextField(default="")
    body = models.TextField()
    post_date = models.DateTimeField(default=datetime.now)
    created_date = models.DateTimeField(default=datetime.now)

    # Implement better datetime with timezones:
    # import pytz
    # from datetime import datetime
    # datetime.utcnow().replace(tzinfo=pytz.utc)

    def save(self, *args, **kwargs):
        self.slug = create_slug(self.title, self.slug, self.post_date)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return u'{%s: %s}' % (self.title, self.body)
