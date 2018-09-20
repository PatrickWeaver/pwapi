from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views
from uploads import views as UploadsViews

urlpatterns = [
  
    path('', views.index, name='index'),
  
    # Projects
    path('projects/', views.projects, name='portfolio-projects-index'),
  
    path('project/new/', csrf_exempt(views.new_project), name='portfolio-project-new'),
    path('projects/new/', csrf_exempt(views.new_project), name='portfolio-projects-new'),
  
    # GET
    path('project/<slug:slug>/', csrf_exempt(views.get_project), name='portfolio-project-get'),
    path('projects/<slug:slug>/', csrf_exempt(views.get_project), name='portfolio-projects-get'),
  
    path('project/<slug:slug>/edit/', csrf_exempt(views.edit_project), name='portfolio-project-edit'),
    path('projects/<slug:slug>/edit/', csrf_exempt(views.edit_project), name='portfolio-projects-edit'),
  
    path('project/<slug:slug>/delete/', csrf_exempt(views.delete_project_by_slug), name='portfolio-project-delete'),
    path('projects/<slug:slug>/delete/', csrf_exempt(views.delete_project_by_slug), name='portfolio-projects-delete'),
  
    path('project/<slug:project_slug>/add-tag/', csrf_exempt(views.add_tag_to_project), name= 'project-add-tag'),
    path('projects/<slug:project_slug>/add-tag/', csrf_exempt(views.add_tag_to_project), name= 'projects-add-tag'),
    path('project/<slug:project_slug>/remove-tag/', csrf_exempt(views.remove_tag_from_project), name= 'project-remove-tag'),
    path('projects/<slug:project_slug>/remove-tag/', csrf_exempt(views.remove_tag_from_project), name= 'projects-remove-tag'),
    path('project-id/<int:id>/delete/', csrf_exempt(views.delete_project_by_id), name='blog-project-by-id-delete'),
  
    # Tags
    path('tags/', views.tags, name='portfolio-tags-index'),
  
    path('tag/new/', csrf_exempt(views.new_tag), name='portfolio-tag-new'),
    path('tags/new/', csrf_exempt(views.new_tag), name='portfolio-tags-new'),
  
    path('tag/<slug:slug>/', views.get_tag, name='portfolio-tag-get'),
    path('tags/<slug:slug>/', views.get_tag, name='portfolio-tags-get'),

    path('tag/<slug:slug>/edit/', csrf_exempt(views.edit_tag), name='portfolio-tag-edit'),
    path('tags/<slug:slug>/edit/', csrf_exempt(views.edit_tag), name='portfolio-tags-edit'),
  
    path('tag/<slug:slug>/delete/', csrf_exempt(views.delete_tag_by_slug), name='portfolio-tag-delete'),
    path('tags/<slug:slug>/delete/', csrf_exempt(views.delete_tag_by_slug), name='portfolio-tags-delete'),
    path('tag-id/<int:id>/delete/', csrf_exempt(views.delete_tag_by_id), name='blog-tag-by-id-delete'),

  
    # Images
    path('images/', views.images, name='portfolio-images-index'),
  
    path('image/new/', csrf_exempt(views.new_image), name='portfolio-image-new'),
    path('images/new/', csrf_exempt(views.new_image), name='portfolio-images-new'),
  
    path('image/<slug:slug>/', views.get_image, name='portfolio-image-get'),
    path('images/<slug:slug>/', views.get_image, name='portfolio-images-get'),

    path('image/<slug:slug>/edit/', csrf_exempt(views.edit_image), name='portfolio-image-edit'),
    path('images/<slug:slug>/edit/', csrf_exempt(views.edit_image), name='portfolio-images-edit'),
  
    path('image/<slug:slug>/delete/', csrf_exempt(views.delete_image_by_slug), name='portfolio-image-delete'),
    path('images/<slug:slug>/delete/', csrf_exempt(views.delete_image_by_slug), name='portfolio-images-delete'),
    path('image-id/<int:id>/delete/', csrf_exempt(views.delete_image_by_id), name='blog-image-by-id-delete'),
  
    path('uploads/', include('uploads.urls'))
]
