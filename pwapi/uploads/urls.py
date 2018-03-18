from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('new/', csrf_exempt(views.new), name='posts'),
]
