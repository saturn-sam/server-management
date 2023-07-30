from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('add', views.add_server, name='add-server'),
    path('add_os', views.add_os, name='add-os'),
    path('add_os_version', views.add_os_version, name='add-os-version'),
    path('add_zone', views.add_zone, name='add-zone'),
    path('add_project', views.add_project, name='add-project'),
    path('add_service2', views.add_service_modal, name='add-service2'),
    path('add_service', views.add_service, name='add-service'),
    path('add_service_type', views.add_service_type, name='add-service-type'),
    path('add_service_group', views.add_service_group, name='add-service-group'),
    path('view_server', views.view_server, name='view-server'),
    path('view_single_server/<int:pk>', views.view_single_server, name='view-single-server'),
    path('view_single_vm/<int:pk>', views.view_single_vm, name='view-single-vm'),
    path('view_rack/', views.view_single_rack, name='view-single-rack'),
    path('edit/server/<int:pk>', views.edit_server, name='edit-server'),
    path('export_server_xls', views.export_server_xls, name='export-server-xls'),
    path('add/vm', views.add_vm, name='add-vm'),
    path('add_vm_loc', views.add_vm_loc, name='add-vm_loc'),
    path('view_vm', views.view_vm, name='view-vm'),
    path('export_vm_xls', views.export_vm_xls, name='export-vm-xls'),
    path('edit/vm/<int:pk>', views.edit_vm, name='edit-vm'),
    path('view/service', views.view_service, name='view-service'),
    path('view_single_service/<int:pk>', views.view_single_service, name='view-single-service'),
    path('add-service', views.add_service, name='add-service'),
    path('edit-service/<int:pk>', views.edit_service, name='edit-service'),
    path('search-server', views.server_report, name='search-server'),\
]