"""pwapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from pwapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/blobs/', include('blobs.urls')),
    path('v1/blog/', include('blog.urls')),
    path('v1/bot/', include('bot.urls')),
    path('v1/people/', include('people.urls')),
    path('v1/portfolio/', include('portfolio.urls')),
    path('v1/uploads/', include('uploads.urls')),

    # Root:
    path('v1/', views.v1, name='v1'),
    path('', views.index, name='index')
]
