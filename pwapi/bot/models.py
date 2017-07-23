from django.db import models

class Guest(models.Model):
    name = models.CharField(max_length=1024)


class IPAddress(models.Model):
    address = models.CharField(max_length=128)

# Which of these systems?
# https://docs.djangoproject.com/en/1.11/topics/db/models/#intermediary-manytomany
# https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
