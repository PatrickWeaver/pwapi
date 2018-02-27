from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('posts/', views.posts, name='posts'),
    path('post/<slug:slug>/', csrf_exempt(views.post), name='post'),
]
