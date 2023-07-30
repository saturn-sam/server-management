from django.contrib import admin
from .models import *
# Register your models here.
# from import_export import resources
# # from core.models import Book

# class VirtualServerResource(resources.ModelResource):

#     class Meta:
#         model = VirtualServer


# from import_export.admin import ImportExportModelAdmin

# class VirtualServerAdmin(ImportExportModelAdmin):
#     resource_classes = [VirtualServerResource]


admin.site.register(OsType)
admin.site.register(OsVersion)
admin.site.register(Zone)
admin.site.register(Project)
admin.site.register(PhysicalServer)
admin.site.register(RunningServices)
admin.site.register(VMLocationType)
admin.site.register(VirtualServer)
admin.site.register(ServiceType)
admin.site.register(ServiceGroup)
admin.site.register(ServerRackInfo)
