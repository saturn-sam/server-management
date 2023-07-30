from email.policy import default
from ipaddress import ip_address
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.

class Secret(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True)
    master_key_name = models.CharField(_("Master Key Name"), default="My Mater Key", max_length=250, blank=False, null=False)
    masterkey_hash = models.TextField(_("Master Password"), blank=False, null=False)
    device_secret = models.TextField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        unique_together = ('master_key_name', 'user_id')

class SecQList(models.Model):
    security_question = models.CharField(_("Enter Security Question"), max_length=250, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.security_question}"

class MySecAnswer(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=False)
    security_question = models.ForeignKey(SecQList, on_delete=models.CASCADE, null=False)
    security_answer = models.TextField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.security_question}"

class Passwd(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, default=None, null=False)
    master_key = models.ForeignKey(Secret, on_delete=models.RESTRICT, null=True)
    site_server_name = models.CharField(_("Site or Servar Name"), max_length=250, blank=False, null=False)
    ip_or_url = models.TextField(_("IP or URL"), blank=False, null=False)
    username = models.TextField(_("Username"), blank=False, null=False)
    password = models.TextField(_("Password"), blank=False, null=False)
    remark = models.TextField(_("Remark"), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.site_server_name}"