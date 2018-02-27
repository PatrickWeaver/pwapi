from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('conversation/([a-zA-Z0-9]+)/', views.conversation, name='conversation'),
    path('guest/([a-zA-Z0-9]+)/', views.guest, name='guest'),
    path('message/', views.message, name='message'),
]
