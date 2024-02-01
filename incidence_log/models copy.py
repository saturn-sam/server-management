from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from knowledgebase.models import KnowledgeBase

# Create your models here.

class Incidence(models.Model):
    """Model for incidents happed"""
    class URGENCY_LEVEL(models.IntegerChoices):
        LOW = 0, 'Low'
        MEDIUM = 1, 'Medium'
        HIGH = 2, 'High'
    
    class IMPACT_LEVEL(models.IntegerChoices):
        CRITICAL = 1, 'High'
        MAJOR = 2, 'Medium'    
        MINOR = 3, 'Low'

    class STATUS(models.IntegerChoices):
        TRIGGERED = 1, 'Triggered'
        ACKNOWLEDGED = 2, 'Acknowledged'    
        RESOLVED = 3, 'Resolved'   

    title = models.CharField(max_length=255, null=False,blank=True)
    urgency = models.IntegerField(choices=URGENCY_LEVEL.choices, default=URGENCY_LEVEL.LOW, null=False,blank=True)
    impact = models.IntegerField(choices=IMPACT_LEVEL.choices, default=IMPACT_LEVEL.MINOR, null=False,blank=True)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.TRIGGERED, null=False,blank=True)
    incidence_description = RichTextUploadingField(blank=True, null=True, help_text = "(Any one from Related KB and Incidence Description is mandatory)")
    related_kb = models.ManyToManyField(KnowledgeBase, help_text = "(Any one from Related KB and Incidence Description is mandatory)")
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_reported_by_user")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_added_by_user")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_updated_by_user")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_deleted_by_user")
    triggered_time = models.DateTimeField(blank=True, null=True)
    responsed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_status = models.IntegerField(blank=False, default=0)
    deleted_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.title}"
    
    # def get_absolute_url(self):
    #     return reverse("core:detailIncident", args=[self.id])


class Resolution(models.Model):
    """Model for incidence resolution"""
    incidence = models.OneToOneField(Incidence, on_delete=models.CASCADE, related_name="resolution")
    resolution = RichTextUploadingField(blank=True, null=True, help_text="(Any one from Related KB and Resolution is mandatory)")
    related_kb = models.ManyToManyField(KnowledgeBase, help_text="(Any one from Related KB and Resolution is mandatory)")
    resolved_by = models.ManyToManyField(settings.AUTH_USER_MODEL)
    resolved_at = models.DateTimeField(blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="resolution_added_by_user")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="resolution_updated_by_user")
    delete_status = models.IntegerField(blank=False, default=0)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="resolution_deleted_by_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.incidence}"