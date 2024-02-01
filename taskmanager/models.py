from django.utils import timezone
from django.db import models

from django.conf import settings


from knowledgebase.models import KnowledgeBase
# from django.forms import Textarea

# Create your models here.
class TaskManager(models.Model):

    task_title = models.CharField(max_length=255,blank=False)
    description = models.TextField(blank=False)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tm_assigned_to")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tm_assigned_by")
    due_date = models.DateTimeField(blank=False, null=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    task_from_incidence = models.BooleanField(default=False)
    task_status = models.IntegerField(blank=False, default=1) # 1 incomplete, 2 complete, 3 incomplete pause, 4 Canceled
    # task_steps_commentary = models.TextField(blank=True)
    task_steps_commentary = models.ManyToManyField('TaskStepComentary', related_name="tmcommentary")
    task_procedure_or_kb = models.ManyToManyField(KnowledgeBase)
    # subtask = models.ManyToManyField('TaskManager', related_name="tmsubtask", null=True, blank=True)
    reference_task = models.ForeignKey('TaskManager', on_delete=models.SET_NULL, related_name="reftask", null=True, blank=True)
    task_visibility = models.IntegerField(blank=True, null=True) # 1 for public, 2 for private 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="taskmanager_created_by_user")
    created_at = models.DateTimeField(default=timezone.now)
    delete_status = models.IntegerField(blank=False, default=0)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="taskmanager_deleted_by_user")

    @property
    def is_past_due(self):
        return timezone.now() > self.due_date

    def __str__(self):
        return f"T{self.id} - {self.task_title}"

class TaskStepComentary(models.Model):
    comment = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="taskstepcomentary_created_by_user")
    add_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Task-comment-added-by-{self.added_by}"

class TaskHistory(models.Model):
    task = models.ForeignKey(TaskManager, on_delete=models.CASCADE, null=False, blank=False)
    new_task_add = models.IntegerField(blank=True,null=True)
    ref_task_add = models.ForeignKey(TaskManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="ref_task_add")
    sub_task_add = models.ForeignKey(TaskManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_task_add")
    task_procedure_or_kb = models.ManyToManyField(KnowledgeBase)
    kb_insert_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="kb_insert_by")
    comment_add = models.ForeignKey(TaskStepComentary, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="th_assigned_to")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="assigned_by_user")
    task_visibility = models.IntegerField(blank=True,null=True)
    due_date = models.IntegerField(blank=True,null=True)
    changed_status = models.CharField(max_length=150,blank=True, null=True)
    effective_date = models.DateTimeField(blank=True, null=True)
    insert_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    insert_date = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return f"H{self.id} - {self.task}"

