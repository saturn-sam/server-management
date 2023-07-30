from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from serverinfo.models import RunningServices, ServiceGroup
# Create your models here.

class LicenseType(models.Model):
    type_name = models.CharField(_("License Type Name"), max_length=250, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True )
    updated = models.DateTimeField( auto_now=True )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="licensetype_createdby", on_delete=models.SET_NULL, null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="licensetype_updatedby", on_delete=models.SET_NULL, null=True, blank=True)
    delete_status = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="licensetype_deleted", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.type_name}"

class LicenseInfo(models.Model):
    license_name = models.CharField(_("License Name"), max_length=250, blank=False, null=False)
    license_number = models.CharField(_("License Number"), max_length=100, blank=True, null=True)
    service_name = models.ForeignKey(RunningServices, related_name="licenseinfo_runningservice", on_delete=models.SET_NULL, blank=True, null=True)
    service_group = models.ForeignKey(ServiceGroup, related_name="licenseinfo_servicegroup", on_delete=models.SET_NULL, blank=True, null=True)
    license_type = models.ForeignKey(LicenseType, on_delete=models.SET_NULL, null=True, blank=True )
    effective_quantity = models.IntegerField(_("Effective Quantity"), blank=False, null=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    license_status = models.BooleanField(_("License Status"), default=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True )
    updated = models.DateTimeField( auto_now=True )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="licenseinfo_createdby", on_delete=models.SET_NULL, null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="licenseinfo_updatedby", on_delete=models.SET_NULL, null=True, blank=True)
    delete_status = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="licenseinfo_deleted", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"License Name: {self.license_name}"
    
class M365License(models.Model):
    user_name = models.CharField(_("User Name"), max_length=250, blank=False, null=False)
    user_id = models.CharField(_("User ID"), max_length=20, blank=False, null=False)
    hostname = models.CharField(_("Hostname"), max_length=20, blank=False, null=False)
    ip_address = models.GenericIPAddressField(_("IP Address"), unique=True, max_length=100, blank=False, null=False)
    branch = models.CharField(_("Branch/Div."), max_length=250, blank=False, null=False)
    date = models.DateTimeField(_("Date"),null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True )
    updated = models.DateTimeField( auto_now=True )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="winlicense_createdby", on_delete=models.SET_NULL, null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="winlicense_updatedby", on_delete=models.SET_NULL, null=True, blank=True)
    delete_status = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="winlicense_deleted", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"User ID: {self.user_id}, Branch: {self.branch}"