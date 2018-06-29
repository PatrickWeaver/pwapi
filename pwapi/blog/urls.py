from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views
from uploads import views as UploadsViews

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('post/<slug:slug>/', csrf_exempt(views.post), name='post'),
    path('uploads/', include('uploads.urls'))
]
