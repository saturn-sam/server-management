from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from knowledgebase.models import KnowledgeBase
from taskmanager.models import *

# Create your models here.

class Incidence(models.Model):
    """Model for incidents happed"""
    class URGENCY_LEVEL(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
    
    class IMPACT_LEVEL(models.IntegerChoices):
        CRITICAL = 1, 'High'
        MAJOR = 2, 'Medium'    
        MINOR = 3, 'Low'

    class STATUS(models.IntegerChoices):
        TRIGGERED = 1, 'Triggered'    
        RESOLVED = 3, 'Resolved'   

    title = models.CharField(max_length=255, null=True,blank=True)
    urgency = models.IntegerField(choices=URGENCY_LEVEL.choices, default=URGENCY_LEVEL.LOW, null=True,blank=True)
    impact = models.IntegerField(choices=IMPACT_LEVEL.choices, default=IMPACT_LEVEL.MINOR, null=True,blank=True)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.TRIGGERED, null=True,blank=True)
    related_kb = models.ManyToManyField(KnowledgeBase, help_text = "(KB about Incidence and Resolution Description.)", blank=True)
    related_task = models.ForeignKey(TaskManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_reported_by_user")
    delete_status = models.IntegerField(blank=False, default=0)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_reported_by_user")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="incidence_assigned_to_user", blank=True)
    resolved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="incidence_resolved_by_user", blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_added_by_user")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_updated_by_user")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_deleted_by_user")
    triggered_time = models.DateTimeField(blank=True, null=True)
    responsed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.title}"
    
    # def get_absolute_url(self):
    #     return reverse("core:detailIncident", args=[self.id])

