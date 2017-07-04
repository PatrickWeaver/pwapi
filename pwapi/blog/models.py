from django.db import models

class Post(models.Model):
    post_title = models.CharField(max_length=1024)
    post_body = models.TextField()
    post_date = models.DateTimeField()
    created_date = models.DateTimeField()

    # Implement better datetime with timezones:
    # import pytz
    # from datetime import datetime
    # datetime.utcnow().replace(tzinfo=pytz.utc)'''

    def __str__(self):
        return u'{%s: %s}' % (self.post_title, self.post_body)
