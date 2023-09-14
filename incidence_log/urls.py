from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
#    path('add_master_pass', views.add_master_pass, name='add_master_pass'),
   path('add_incidence', views.add_incidence, name='add_incidence'),

]