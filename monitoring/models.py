from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from serverinfo.models import RunningServices
from django.utils import timezone
class Log(models.Model):
    STATUS_FROM_CHOICE = (
        ('auto', 'Auto'),
        ('Manual', 'Manual'),
    )
    
    service = models.ForeignKey(RunningServices, on_delete=models.RESTRICT, null=False, blank=False)
    # status = models.IntegerField(_("Status"), blank=False)
    mod_time = models.DateTimeField(blank=False, null=False)
    status_from = models.CharField(max_length=20, choices=STATUS_FROM_CHOICE, blank=False, null=False)
    server_ip = models.GenericIPAddressField(default="0.0.0.0", blank=False, null=False)
    # unpublish_status = models.BooleanField(default=False,null=False)
    manually_inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="manually_inserted_by_user", on_delete=models.CASCADE, blank=True, null=True)
    insertion_date = models.DateTimeField(blank=False, null=False)

    @property
    def is_mod_time_gt_five_min(self):
        time_diff = timezone.localtime(timezone.now()) - timezone.localtime(self.mod_time)
        # if time_diff.total_seconds() > 300:
        return time_diff.total_seconds() > 300

    @property
    def is_log_time_gt_five_min(self):
        time_diff = timezone.localtime(timezone.now()) - timezone.localtime(self.insertion_date)
        # if time_diff.total_seconds() > 300:
        return time_diff.total_seconds() > 300     

    def __str__(self):
        return f"Log of- {self.service.service_name}"