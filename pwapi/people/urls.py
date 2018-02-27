from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('',  views.people, name='people'),
    path('authenticate/', csrf_exempt(views.authenticate), name='authenticate'),
]
