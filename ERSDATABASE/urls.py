from django.contrib import admin
from django.urls import path,include
from ers import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.user_login, name='Login'),
    path('home/', views.homepage, name='Home'),
    path('home/details1/', views.details1, name='Details1'),
    path('home/details/', views.details, name='Details'),
    path('home/register/',views.register,name="Register"),
    path('home/details2/', views.details2, name='Details2'),
    path('home/details3/', views.details3, name='Details3'),
    path('home/unregister/',views.unregister,name="Unegister"),
    path('home/survey1/',views.survey1,name="Survey1"),
    path('home/survey/',views.survey,name="Survey"),
    path('administrator/', include('admin1.urls')),  
    
]
