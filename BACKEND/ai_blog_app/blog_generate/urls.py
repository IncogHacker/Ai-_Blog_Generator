

from django.urls import path

from . import views

# Django module that handles URL routing
# A function used to connect URL → view
#From dot mean current folder

urlpatterns = [


     # path(route, view, kwargs=None, name=None)
     #Home Page
     path('',views.index,name='index'),

     path('login',views.user_login,name='login'),

     path('Signup',views.user_signup,name='Signup'),


     path('logs',views.user_logout, name='logs'),

     path('generate-blog',views.generate_blog, name='generate-blog')

     
]


