from django.urls import include, path

from . import views
from uploads import views as UploadsViews

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    #path('project/<slug:slug>/', csrf_exempt(views.project), name='project'),
    path('uploads/', include('uploads.urls'))
]
