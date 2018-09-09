from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views
from uploads import views as UploadsViews

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='portfolio-projects-index'),
  
    path('project/new/', csrf_exempt(views.new_project), name='portfolio-project-new'),
    path('projects/new/', csrf_exempt(views.new_project), name='portfolio-projects-new'),
  
    # GET
    path('project/<slug:slug>/', csrf_exempt(views.get_project), name='portfolio-project-get'),
    path('projects/<slug:slug>/', csrf_exempt(views.get_project), name='portfolio-projects-get'),
  
    path('project/<slug:slug>/edit/', csrf_exempt(views.edit_project), name='portfolio-project-edit'),
    path('projects/<slug:slug>/edit/', csrf_exempt(views.edit_project), name='portfolio-projects-edit'),
  
    path('project/<slug:slug>/delete/', csrf_exempt(views.delete_project), name='portfolio-project-delete'),
    path('projects/<slug:slug>/delete/', csrf_exempt(views.delete_project), name='portfolio-projects-delete'),
  
    path('project/<slug:project_slug>/add-tag/', csrf_exempt(views.add_tag_to_project), name= 'project-add-tag'),
    path('project/<slug:project_slug>/remove-tag/', csrf_exempt(views.remove_tag_from_project), name= 'project-remove-tag'),
  
    path('tags/', views.tags, name='portfolio-tags-index'),
  
    path('tag/new/', csrf_exempt(views.new_tag), name='portfolio-tag-new'),
    path('tags/new/', csrf_exempt(views.new_tag), name='portfolio-tags-new'),
  
    path('tag/<slug:slug>/', views.get_tag, name='portfolio-tag-get'),
    path('tags/<slug:slug>/', views.get_tag, name='portfolio-tags-get'),

    path('tag/<slug:slug>/edit/', csrf_exempt(views.edit_tag), name='portfolio-tag-edit'),
    path('tags/<slug:slug>/edit/', csrf_exempt(views.edit_tag), name='portfolio-tags-edit'),
  
    path('tag/<slug:slug>/delete/', csrf_exempt(views.delete_tag), name='portfolio-tag-delete'),
    path('tags/<slug:slug>/delete/', csrf_exempt(views.delete_tag), name='portfolio-tags-delete'),

    path('images/', views.images, name='portfolio-images-index'),
    path('uploads/', include('uploads.urls'))
]
