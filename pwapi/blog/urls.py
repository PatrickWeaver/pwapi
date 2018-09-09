from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views
from uploads import views as UploadsViews

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('posts/', views.posts, name='blog-posts-index'),

    path('post/new/', csrf_exempt(views.new_post), name='blog-post-new'),
    path('posts/new/', csrf_exempt(views.new_post), name='blog-posts-new'),
  
    path('post/<slug:slug>/', csrf_exempt(views.get_post), name='blog-post-get'),
    path('posts/<slug:slug>/', csrf_exempt(views.get_post), name='blog-posts-get'),
  
    path('post/<slug:slug>/edit/', csrf_exempt(views.edit_post), name='blog-post-edit'),
    path('posts/<slug:slug>/edit/', csrf_exempt(views.edit_post), name='blog-posts-edit'),
  
    path('post/<slug:slug>/delete/', csrf_exempt(views.delete_post), name='blog-post-delete'),
    path('posts/<slug:slug>/delete/', csrf_exempt(views.delete_post), name='blog-posts-delete'),
    path('post-id/<int:id>/delete/', csrf_exempt(views.delete_post_by_id), name='blog-post-by-id-delete'),
  
    path('uploads/', include('uploads.urls'))
]