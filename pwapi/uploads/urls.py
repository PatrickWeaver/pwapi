from django.urls import path
#from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('new/', views.new, name='posts'),
]
