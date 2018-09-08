from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views
from uploads import views as UploadsViews

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),

    path('post/new/', csrf_exempt(views.new_post), name='post'),
    path('posts/new/', csrf_exempt(views.new_post), name='post'),
  
    path('post/<slug:slug>/', csrf_exempt(views.get_post), name='post'),
    path('posts/<slug:slug>/', csrf_exempt(views.get_post), name='post'),
  
    path('post/<slug:slug>/edit/', csrf_exempt(views.edit_post), name='post'),
    path('posts/<slug:slug>/edit/', csrf_exempt(views.edit_post), name='post'),
  
    path('post/<slug:slug>/delete/', csrf_exempt(views.delete_post), name='post'),
    path('posts/<slug:slug>/delete/', csrf_exempt(views.delete_post), name='post'),
  
    path('uploads/', include('uploads.urls'))
]