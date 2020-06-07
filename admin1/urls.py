from django.contrib import admin
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.conf import settings

urlpatterns = [  
        path('', views.adminpage, name='Admin'),
        path('create-event/', views.createevent, name='Create Event'),
        path('edit-event1/', views.modifyevent1, name='Edit Event'),
        path('edit-event/', views.modifyevent, name='Edit Event'),
        path('delete-event/', views.deleteevent, name='Delete Event'),
        path('edit-survey1/', views.createsurvey1, name='Edit Survey'),
        path('edit-survey/', views.createsurvey, name='Edit Survey'),
        path('edit-survey/add/', views.addsurvey, name='Add Survey'),
        path('delete-question/', views.deletequestion, name='Delete Question'),
        path('registrants1/', views.registrants1, name="Registrants1"),
        path('registrants/', views.registrants,name="Registrants"),
        path('response1/',views.response1, name="Response1"), 
        path('response/',views.response, name="Response"),
        path('add-student/', views.addstudent, name = 'Add Student'),
        path('edit-student1/', views.modifystudent1, name='Edit Student'),
        path('edit-student/', views.modifystudent, name='Edit Student'),
        path('delete-student/', views.deletestudent, name='Delete Student'),
        
]