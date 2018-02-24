"""pwapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from pwapi import views
from blog import views as blog_views
from bot import views as bot_views
from people import views as people_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Blog:
    url(r'^blog/posts/new/$', csrf_exempt(blog_views.new_post), name='new_post'),
    url(r'^blog/posts/$', blog_views.posts, name='posts'),
    url(r'^blog/post/$', blog_views.post, name='post'),

    # Bot:
    url(r'^bot/conversation/([a-zA-Z0-9]+)/$', bot_views.conversation, name='conversation'),
    url(r'^bot/guest/([a-zA-Z0-9]+)/$', bot_views.guest, name='guest'),
    url(r'^bot/message/$', bot_views.message, name='message'),


    # People:
    url(r'^people/$', people_views.people, name='people'),
    url(r'^people/authenticate/$', csrf_exempt(people_views.authenticate), name='authenticate'),

    # Root:
    url(r'^$', views.index, name='index'),
]
