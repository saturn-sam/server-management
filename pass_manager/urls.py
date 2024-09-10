from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('add_master_pass', views.add_master_pass, name='add_master_pass'),
    path('my_master_pass', views.my_master_pass, name='my_master_pass'),
    path('change_master_pass', views.change_master_pass, name='change_master_pass'),
    path('add_entry', views.add_entry, name='add_entry'),
    path('edit_entry/<int:pk>', views.edit_entry, name='edit_entry'),
    path('pass_list', views.pass_list, name='pass_list'),
    path('view_pass', views.view_pass, name='view_pass'),
    path('delete_entry', views.delete_entry, name='delete_entry'),
]