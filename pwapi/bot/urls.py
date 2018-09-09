from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('conversation/([a-zA-Z0-9]+)/', views.conversation, name='bot-conversation-get'),
    path('conversations/([a-zA-Z0-9]+)/', views.conversation, name='bot-conversations-get'),
    path('guest/([a-zA-Z0-9]+)/', views.guest, name='bot-guest-get'),
    path('guests/([a-zA-Z0-9]+)/', views.guest, name='bot-guests-get'),
    path('message/', views.message, name='bot-message'),
]
