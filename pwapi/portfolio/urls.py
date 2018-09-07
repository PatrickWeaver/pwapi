from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views
from uploads import views as UploadsViews

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', csrf_exempt(views.project), name='project'),
    path('projects/<slug:slug>/', csrf_exempt(views.project), name='project'),
    path('tags/', views.tags, name='tags'),
    path('tag/<slug:slug>/', csrf_exempt(views.tag), name='tag'),
    path('tags/<slug:slug>/', csrf_exempt(views.tag), name='tag'),
    path('images/', views.images, name='images'),
    path('uploads/', include('uploads.urls'))
]
