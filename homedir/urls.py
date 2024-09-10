from django.contrib import admin
from django.urls import path, include
#from .views import PostListView
from . import views
from authentication.views import home_page, ProfileEditView

urlpatterns = [
    path('', home_page, name='home'),
    path('edit-profile/<int:pk>/', ProfileEditView.as_view(), name='edit-profile'),
    # path('get-task-count/', get_task_count, name='get-task-count'),
    # path('edit-profile', views_a.profileedit, name='profile-edit'),
]