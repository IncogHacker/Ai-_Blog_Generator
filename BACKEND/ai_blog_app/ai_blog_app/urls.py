"""
URL configuration for ai_blog_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from os import stat

from django.contrib import admin
# This imports Django’s built-in admin system.

from django.urls import path ,include

from django.conf import settings

from django.conf.urls.static import static
# static() is used in Django to serve media or static files from a specified folder during development.
# Browser asks → image/video/audio
# Django → "I don't know where it is"

# Browser asks → Django finds file → sends it when i use static

#This Urls Help to call Blog generator Urls that present in app
urlpatterns = [

    path('admin/', admin.site.urls),

    path('',include('blog_generate.urls'))
     #means At root URL(' ') → use blog_generate URLs
     #  # this tells Go into the Blog_generate app look for the urls files and look for home page # app connected here
]

urlpatterns=urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# static() returns a list of URL patterns, so we use += to append them to existing urlpatterns list.

# http://localhost:8000/media/audio.mp3  --setting.media_Url
# /media/ → check MEDIA_ROOT folder → find audio.mp3 → send file


