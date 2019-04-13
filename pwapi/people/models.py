from django.db import models
import random, string

def generate_api_key():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])

class Person(models.Model):
    username = models.CharField(max_length=50, unique=True)
    client_id = models.CharField(default=generate_api_key, max_length=255, unique=True, blank=True)
    hashed_password = models.BinaryField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    api_key = models.CharField(default=generate_api_key, max_length=255, unique=True, blank=True)
    
    index_fields = [
      'username',
      'name',
      'email'
    ]
    required_fields = ['username', 'name', 'email', 'password']
    allowed_fields = [] + required_fields
    
    hide_if = None

    allowed_filters = []
    
    api_path = '/v1/people/'
    api_identifier = 'username'
    def get_api_url(self, request):
      return request.scheme + "://" + request.get_host() + self.api_path + getattr(self, self.api_identifier, '')
    

    def __str__(self):
        return u'{%s [%s]}' % (self.username, self.email)
      
    def admin_view(self):
        return {
          #"id": self.id,
          "username": self.username,
          "id": self.client_id,
          "name": self.name,
          "email": self.email,
          "api_key": self.api_key
        }
