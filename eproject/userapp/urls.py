from django.contrib import admin
from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('registration/', registration, name='registration'),
  path('login/', auth_views.LoginView.as_view(template_name='userapp/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'), 
  path('profiledetails/', profiledetails, name='profiledetails'),
  path('profileupdate/', profileupdate, name='profileupdate'),
]