from django.contrib import admin
from django.urls import path,include


from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
        path('insert-license', views.insert_license, name='insert-license'),
        path('view-license', views.view_license, name='view-license'),
        path('download-license-list', views.download_license_list, name='download-license-list'),
        path('add-license-type', views.add_license_type, name='add-license-type'),
        path('view-license-summary', views.view_license_summary, name='view-license-summary'),
        path('download-license-summary', views.download_license_summary, name='download-license-summary'),
        path('edit-license/<int:pk>', views.edit_license, name='edit-license'),
        path('add-m365-license', views.add_m365_license, name='add-m365-license'),
        path('view-m365-license', views.view_m365_license, name='view-m365-license'),
        path('delete-m365-license', views.delete_m365_license, name='delete-m365-license'),
]
