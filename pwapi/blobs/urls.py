from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.blobs, name='blobs-index'),
    path('blob-id/<int:id>/delete/', csrf_exempt(views.delete_blob_by_id), name='blog-delete-by-id'),
    path('new/', csrf_exempt(views.new_blob), name='blob-new'),
    path('<slug:slug>/', csrf_exempt(views.get_blob), name='blog-get'),
    path('<slug:slug>/edit/', csrf_exempt(views.edit_blob), name='blob-edit'),
    path('<slug:slug>/delete/', csrf_exempt(views.delete_blob_by_slug), name='blob-delete-by-slug'),

]