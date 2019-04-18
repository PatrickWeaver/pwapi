from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('',  views.people, name='people-index'),
    #path('person/', csrf_exempt(views.person), name='person'),
    path('new/', csrf_exempt(views.new_person), name='people-new'),
    path('authenticate/', csrf_exempt(views.authenticate), name='people-authenticate'),
]
