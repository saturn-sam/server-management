from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

from knowledgebase.models import KnowledgeBase

# Create your models here.

class Incident(models.Model):
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


    urgency = models.IntegerField(choices=URGENCY_LEVEL.choices, default=URGENCY_LEVEL.LOW)
    impact = models.IntegerField(choices=IMPACT_LEVEL.choices, default=IMPACT_LEVEL.MINOR)
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.TRIGGERED)
    title = models.CharField(max_length=255)
    incidence_description = RichTextUploadingField(blank=True, null=True)
    resolution = RichTextUploadingField(blank=True, null=True)
    related_kb = models.ManyToManyField(KnowledgeBase)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_reported_by_user")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_assigned_to_user")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_created_by_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_updated_by_user")
    updated_at = models.DateTimeField(auto_now=True)
    delete_status = models.IntegerField(blank=False, default=0)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidence_deleted_by_user")
    deleted_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.title}"
    
    # def get_absolute_url(self):
    #     return reverse("core:detailIncident", args=[self.id])


# class Resolution(models.Model):
#     """Model for incidents happed"""
#     incidence = models.OneToOneField(Incident, on_delete=models.CASCADE, related_name="resolution")
    