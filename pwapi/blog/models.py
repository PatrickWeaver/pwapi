from django.db import models

def create_slug(title, post_date):
    print("CREATE SLUG")
    print(title)
    print(title.replace(' ', '-').lower())
    return title.replace(' ', '-').lower()


class Post(models.Model):
    title = models.CharField(max_length=1024)
    slug = models.CharField(max_length=1024, unique=True)
    body = models.TextField()
    post_date = models.DateTimeField()
    created_date = models.DateTimeField()

    # Implement better datetime with timezones:
    # import pytz
    # from datetime import datetime
    # datetime.utcnow().replace(tzinfo=pytz.utc)

    def save(self, *args, **kwargs):
        self.slug = create_slug(self.title, self.post_date)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return u'{%s: %s}' % (self.title, self.body)
