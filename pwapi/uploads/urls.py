from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.root, name='uploads-root'),
    path('new/', csrf_exempt(views.new), name='uploads-new'),
]
