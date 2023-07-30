from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TaskManager)
admin.site.register(TaskStepComentary)
admin.site.register(TaskHistory)

