from django.contrib import admin
from django.urls import path, include

from .views import task_create, private_task_create, task_list, task_view, add_comment, change_status,change_assign_to, change_ref_task, change_due_date, change_kb, change_visibility, search_task, user_and_category_wise_report

urlpatterns = [
#     path('', home_page, name='kb-home'),
    path('add-task', task_create, name='add-task'),
    path('add-private-task', private_task_create, name='add-private-task'),
    path('task-list', task_list, name='task-list'),
    path('task/<int:pk>/view/', task_view, name='task-view'),
    path('search-task', search_task, name='search-task'),
    path('add-comment', add_comment, name='add-comment'),
    path('change-status', change_status, name='change-status'),
    path('change-visibility', change_visibility, name='change-visibility'),
    path('change-assign-to', change_assign_to, name='change-assign-to'),
    path('change-ref-task', change_ref_task, name='change-ref-task'),
    path('change-due-date', change_due_date, name='change-due-date'),
    path('change-kb', change_kb, name='change-kb'),
    path('user_cat_report', user_and_category_wise_report, name='user_cat_report'),
#     path('knowledge/<int:pk>-<str:slug>/', KBDetailView, name='kb-details'),
#     path('<int:pk>-<str:slug>/Preview/', kbpreview, name='kb-preview'),
#     path('like', like_post, name='like-post'),
#     path('my-kb', my_kb, name='my-kb'),
#     path('edit-kb/<int:pk>-<str:slug>/', KBEditView.as_view(), name='edit-kb'),
#     path('add-kb-topic', KBTopicAddView.as_view(), name='add-kb-topic'),
#     path('share-kb', share_kb, name='share-kb'),
#     path('unshare-kb', unshare_kb, name='unshare-kb'),
#     path('shared-with-me', shared_with_me, name='shared-with-me'),
#     path('all-kb', all_kb, name='all-kb'),
]