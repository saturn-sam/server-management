from django.contrib import admin
from django.urls import path, include
#from .views import PostListView
from .views import home_page, KBCreateView, KBDetailView, like_post, my_kb, KBEditView, KBTopicAddView, kbpreview, share_kb, unshare_kb, shared_with_me, all_kb

urlpatterns = [
    path('', home_page, name='kb-home'),
    path('add-kb', KBCreateView.as_view(), name='add-kb'),
    path('knowledge/<int:pk>-<str:slug>/', KBDetailView, name='kb-details'),
    path('<int:pk>-<str:slug>/Preview/', kbpreview, name='kb-preview'),
    path('like', like_post, name='like-post'),
    path('my-kb', my_kb, name='my-kb'),
    path('edit-kb/<int:pk>-<str:slug>/', KBEditView.as_view(), name='edit-kb'),
    path('add-kb-topic', KBTopicAddView.as_view(), name='add-kb-topic'),
    path('share-kb', share_kb, name='share-kb'),
    path('unshare-kb', unshare_kb, name='unshare-kb'),
    path('shared-with-me', shared_with_me, name='shared-with-me'),
    path('all-kb', all_kb, name='all-kb'),
]