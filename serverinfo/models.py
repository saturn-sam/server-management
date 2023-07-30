from email.policy import default
from django.db import models
# from django.db.models.fields import IntegerField
# from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import datetime


from django.conf import settings
# Create your models here.


class OsType(models.Model):
    os_type = models.CharField(_("OS Type"), max_length=150, blank=False, null=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null="True")
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="os_type_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.os_type}"

class OsVersion(models.Model):
    os_version = models.CharField(_("OS Version"), max_length=150, blank=False, null=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null="True")
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="os_version_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    # delete_time = models.DateTimeField(default=datetime.datetime(1970,1,1))
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.os_version}"

class Zone(models.Model):
    zone = models.CharField(_("Zone"), max_length=150, blank=False, null=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null="True")
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="zone_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.zone}"

class Project(models.Model):
    project = models.CharField(_("Project Title"), max_length=250, blank=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null="True")
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="project_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.project}"

class ServiceType(models.Model):
    service_type_name = models.CharField(_("Service Type"), unique=True, max_length=250, blank=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True)
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="service_type_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_type_name}"

class ServiceGroup(models.Model):
    service_group_name = models.CharField(_("Service Group"), unique=True, max_length=250, blank=False, null=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True)
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="service_group_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_group_name}"

class RunningServices(models.Model):
    RES_TEAM=(
        ('System', 'System'),
        ('Network', 'Network'),
        ('Security', 'Security'),
        ('DBA', 'DBA'),
        ('SDD', 'SDD'),
        ('Card', 'Card'),
        ('IPT', 'IPT'),
        ('BACH', 'BACH'),
        ('Others', 'Others')
    )
    service_name = models.CharField(_("Service Name"), unique=True, max_length=250, blank=False, null=False)
    service_type = models.ForeignKey(ServiceType, on_delete=models.RESTRICT, null=False, blank=False)
    service_group = models.ForeignKey(ServiceGroup, on_delete=models.RESTRICT, null=True, blank=True)
    service_ip = models.CharField(_("Service IP"), max_length=100, blank=True, null=True)
    service_file_loc =  models.CharField(_("Service File Location"), max_length=250, blank=True, null=True)
    service_owner = models.CharField(_("Service Owner"), max_length=250, choices = RES_TEAM, blank=False, null=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True)
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="running_service_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_name}"

class PhysicalServer(models.Model):

    server_name = models.CharField(_("Server Name"), unique=True, max_length=150, blank=False, null=False)
    os_type = models.ForeignKey(OsType, on_delete=models.RESTRICT, related_name="physical_server", blank=False, null=False)
    os_version = models.ForeignKey(OsVersion, on_delete=models.RESTRICT, related_name="physical_server", blank=False, null=False)
    server_type = models.CharField(_("Server Type"), max_length=10, blank=True, null=True)
    service_name = models.ManyToManyField(RunningServices, related_name="physical_server", blank=True, null=True)
    # service_type = models.ForeignKey(ServiceType, on_delete=models.RESTRICT, related_name="physical_server", blank=False, null=False)
    idrac_ip = models.GenericIPAddressField(_("IDrac IP"), unique=True, max_length=100, blank=True, null=True)
    primary_ip = models.GenericIPAddressField(_("Primary IP"), unique=True, max_length=100, blank=False, null=False)
    secondary_ip = models.CharField(_("Other IP"), unique=True, max_length=100, blank=True, null=True)
    public_ip = models.GenericIPAddressField(_("Public IP"), unique=True, max_length=100, blank=True, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.RESTRICT, blank=False, null=False)
    brand = models.CharField(_("Brand"), max_length=100, blank=False, null=False)
    model = models.CharField(_("Model"), max_length=100, blank=False, null=False)
    service_tag = models.CharField(_("Service Tag"), unique=True, default="NULL", max_length=100, blank=False, null=False)
    asset_code = models.CharField(_("Asset Code"), unique=True, default="NULL", max_length=100, blank=False, null=False)
    ram = models.IntegerField(_("RAM(GB)"), blank=True, null=True)
    no_of_hdd = models.IntegerField(_("Hard Disk Count"), blank=True, null=True)
    total_storage = models.IntegerField(_("Total Usable Storage(GB)"), blank=True, null=True)
    processor_core = models.IntegerField(_("Processor Core"), blank=True, null=True)
    # server_receive_date = models.DateField(_("Server Receive Date"), default=datetime.date.today, blank=True, null=True)
    # warranty_expiry_date = models.DateField(_("Warranty Expiry Date"), default=datetime.datetime.now()+datetime.timedelta(days=1095), blank=True, null=True)
    server_receive_date = models.DateField(_("Server Receive Date"), blank=True, null=True)
    warranty_expiry_date = models.DateField(_("Warranty Expiry Date"), blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT, blank=True, null=True)
    vendor_name = models.CharField(_("Vendor Name"), unique=True, max_length=100, blank=True, null=True)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null="True")
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="pysical_server_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return f"Server: {self.server_name}, IP: {self.primary_ip}"

class ServerRackInfo(models.Model):
    FORMFACTOR=(
    (1, '1U'),
    (2, '2U'),
    (3, '3U'),
    (4, '4U'),
    (5, '5U'),
    )
    SERVER_STATUS=(
        ('On', 'On'),
        ('Off', 'Off'),
        ('Faulty', 'Faulty')
    )
    LOCATION = (
        ('dc', 'DC'),
        ('dr', 'DR'),
    )
    server = models.ForeignKey(PhysicalServer, on_delete=models.CASCADE, related_name="server_rack_info", null="False", blank="False")
    location = models.CharField(_("Server Location"), default="dc", max_length=10, choices = LOCATION, blank=False, null=False)
    rack = models.IntegerField(_("Rack No."), blank=False, null=False)
    loc_in_rack = models.IntegerField(_("Server Location in Rack."), blank=False, null=False)
    form_factor = models.IntegerField(_("Form Factor"), choices = FORMFACTOR, blank=False, null=False)
    server_run_status = models.CharField(_("Server Status"), max_length=250, choices = SERVER_STATUS, blank=False, null=False)

    class Meta:
        unique_together = ['location','rack', 'loc_in_rack']

    def __str__(self):
        return f"Server: {self.server}, Rack: {self.rack}"    

class VMLocationType(models.Model):
    container = models.CharField(_("VM Location Type"), max_length=250, blank=False)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null="True")
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="vm_location_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)    
    def __str__(self):
        return f"{self.container}"

class VirtualServer(models.Model):
    LOCATION = (
        ('dc', 'DC'),
        ('dr', 'DR'),
    )

    server_name = models.CharField(_("Server Name"), max_length=150, blank=False, null=False)
    location = models.CharField(_("Server Location"), max_length=10, choices = LOCATION, blank=False, null=False)
    vm_location_type = models.ForeignKey(VMLocationType, on_delete=models.RESTRICT, blank=False, null=False)
    vm_location = models.ForeignKey(PhysicalServer, on_delete=models.RESTRICT, max_length=250, blank=True, null=True)
    os_type = models.ForeignKey(OsType, on_delete=models.RESTRICT, related_name="vm_os_version", blank=False, null=False)
    os_version = models.ForeignKey(OsVersion, on_delete=models.RESTRICT, related_name="vm_os_version", blank=False, null=False)
    server_type = models.CharField(_("Server Type"), max_length=10, blank=True, null=True)
    service_name = models.ManyToManyField(RunningServices, related_name="vm_runs_server", blank=True, null=True)
    primary_ip = models.GenericIPAddressField(_("Primary IP"), unique=True, max_length=100, blank=False, null=False)
    secondary_ip = models.CharField(_("Other IP"), unique=True, max_length=100, blank=True, null=True)
    public_ip = models.GenericIPAddressField(_("Public IP"), unique=True, max_length=100, blank=True, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.RESTRICT, blank=False, null=False)
    ram = models.IntegerField(_("RAM(GB)"), blank=True, null=True)
    no_of_hdd = models.IntegerField(_("Hard Disk Count"), blank=True, null=True)
    total_storage = models.IntegerField(_("Total Usable Storage(GB)"), blank=True, null=True)
    processor_core = models.IntegerField(_("Processor Core"), blank=True, null=True)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null="True")
    update_time = models.DateTimeField(default=timezone.now)
    delete_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="virtual_server_delete_user", on_delete=models.RESTRICT, null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return f"Server: {self.server_name}, IP: {self.primary_ip}"



    
