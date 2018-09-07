from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views
from uploads import views as UploadsViews

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
  
    path('project/new/', csrf_exempt(views.new_project), name='project'),
    path('projects/new/', csrf_exempt(views.new_project), name='project'),
  
    # GET
    path('project/<slug:slug>/', csrf_exempt(views.project), name='project'),
    path('projects/<slug:slug>/', csrf_exempt(views.project), name='project'),
  
    path('project/<slug:slug>/edit/', csrf_exempt(views.edit_project), name='project'),
    path('projects/<slug:slug>/edit/', csrf_exempt(views.edit_project), name='project'),
  
    path('project/<slug:slug>/delete/', csrf_exempt(views.delete_project), name='project'),
    path('projects/<slug:slug>/delete/', csrf_exempt(views.delete_project), name='project'),
  
    path('tags/', views.tags, name='tags'),
    path('tag/<slug:slug>/', csrf_exempt(views.tag), name='tag'),
    path('tags/<slug:slug>/', csrf_exempt(views.tag), name='tag'),
    path('images/', views.images, name='images'),
    path('uploads/', include('uploads.urls'))
]
