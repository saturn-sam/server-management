from django import forms
from django.forms import ModelChoiceField, ModelForm
# from django.db.models import Q
from .models import TaskManager, TaskType
from django.core.exceptions import ValidationError

from django.conf import settings

from authentication.models import CustomUser

class UserFullnameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class UserMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom multiple select Feild with full name
    """
    def label_from_instance(self, obj):
          return obj.get_full_name()

class UserMultipleChoiceField2(ModelChoiceField):
    """
    Custom multiple select Feild with full name
    """
    def label_from_instance(self, obj):
          return obj
    


class TMCreateForm(ModelForm):

    class Meta:
        model = TaskManager
        fields = ['task_title', 'task_type', 'description','assigned_to','assigned_by','due_date', 'reference_task']

    def __init__(self,*args, **kwargs):
        super(TMCreateForm, self).__init__(*args, **kwargs)
        TASK_STATUSES = [
            (2,'Complete'),
            (1, 'Incomplete')
        ]
        # self.fields['assigned_to'] = UserFullnameChoiceField(queryset=CustomUser.objects.filter(is_active=True))
        self.fields['assigned_to'] = UserMultipleChoiceField(queryset=CustomUser.objects.filter(is_active=True).order_by('email'))
        self.fields['assigned_by'] = UserFullnameChoiceField(queryset=CustomUser.objects.filter(is_active=True))
        self.fields['reference_task'].queryset = TaskManager.objects.filter(delete_status=0, task_visibility=1)
        self.fields['task_status'] = forms.ChoiceField(choices=TASK_STATUSES)
        # print(CustomUser.objects.filter(pk = user.id))
        # self.fields['assigned_by'].initial = CustomUser.objects.filter(pk = user.id)


class PrivateTMCreateForm(ModelForm):
    class Meta:
        model = TaskManager
        fields = ['task_title', 'description','due_date', 'reference_task']

    # def __init__(self,*args, **kwargs):
    #     super(PrivateTMCreateForm, self).__init__(*args, **kwargs)

    #     # self.fields['assigned_to'] = UserFullnameChoiceField(queryset=CustomUser.objects.filter(is_active=True))
    #     self.fields['assigned_to'] = UserMultipleChoiceField(queryset=CustomUser.objects.filter(is_active=True).order_by('email'))
    #     self.fields['assigned_to'].required = False
    #     self.fields['assigned_by'] = UserFullnameChoiceField(queryset=CustomUser.objects.filter(is_active=True))
    #     self.fields['assigned_by'].required = False

    # def clean(self):
    #     title = self.cleaned_data.get('title')
    #     if TaskManager.objects.filter(title=title).exists():
    #         raise ValidationError(f'KB with Title  "{title}" alredy exists. Please change the title.')



class TaskReportForm(forms.Form):
    # class Meta:
    #     model = TaskManager
    #     fields = ['assigned_to', 'assigned_by', 'task_type', 'created_at','completed_date']
    # def __init__(self, *args, **kargs):
    #     super(TaskReportForm, self).__init__(*args, **kargs)
    TASK_STATUSES = [
        (2,'Complete'),
        (1, 'Incomplete'),
        (3, 'Incomplete Pause'),
        (4, 'Cancelled')
    ]
    #     self.fields['task_type'] = forms.ModelMultipleChoiceField(queryset=TaskType.objects.all(),required=False)
    #     self.fields['assigned_to'] = UserMultipleChoiceField(queryset=CustomUser.objects.filter(is_active=True).order_by('email'),required=False)
    #     self.fields['assigned_by'] = UserMultipleChoiceField(queryset=CustomUser.objects.filter(is_active=True),required=False)
    #     self.fields['task_status'] = forms.MultipleChoiceField(choices=TASK_STATUSES,required=False)
    #     self.fields['summary_report'] = forms.BooleanField(required=False)
    #     self.fields['created_at'] = forms.DateTimeField(required=False)
    #     self.fields['completed_date'] = forms.DateTimeField(required=False)
    task_type = forms.ModelMultipleChoiceField(queryset=TaskType.objects.all(),required=False)
    assigned_to  = UserMultipleChoiceField(queryset=CustomUser.objects.filter(is_active=True).order_by('email'),required=False)
    assigned_by = UserMultipleChoiceField(queryset=CustomUser.objects.filter(is_active=True),required=False)
    task_status = forms.MultipleChoiceField(choices=TASK_STATUSES,required=False)
    summary_report = forms.BooleanField(required=False)
    created_at = forms.DateField(required=False)
    completed_date = forms.DateField(required=False)
    # def clean(self):
    #     super(TaskReportForm, self).clean()

