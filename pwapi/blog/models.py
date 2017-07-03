from django.db import models

class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_body = models.TextField()
    post_date = models.DateField()
    created_date = models.DateField()

    def __str__(self):
        return u'{%s: %s}' % (self.post_title, self.post_body)
