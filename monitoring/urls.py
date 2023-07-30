from django.contrib import admin
from django.urls import path,include


from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.monitoring_dashboard, name='monitoring_dashboard'),
    path('collection', views.collection, name='collection'),
]
