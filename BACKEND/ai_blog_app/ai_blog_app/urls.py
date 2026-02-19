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
from django.contrib import admin
# This imports Django’s built-in admin system.

from django.urls import path ,include

#This Urls Help to call Blog generator Urls that present in app
urlpatterns = [

    path('admin/', admin.site.urls),

    path('',include('blog_generate.urls'))
     #means At root URL(' ') → use blog_generate URLs
     #  # this tells Go into the Blog_generate app look for the urls files and look for home page # app connected here
]
