from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(KBTopic)
admin.site.register(KnowledgeBase)
admin.site.register(Comment)
admin.site.register(KBViews)

