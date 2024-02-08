from django import forms
from django.forms import ModelChoiceField, ModelForm
# from django.db.models import Q
from .models import TaskManager
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
        fields = ['task_title', 'description','assigned_to','assigned_by','due_date', 'reference_task']

    def __init__(self,*args, **kwargs):
        super(TMCreateForm, self).__init__(*args, **kwargs)

        # self.fields['assigned_to'] = UserFullnameChoiceField(queryset=CustomUser.objects.filter(is_active=True))
        self.fields['assigned_to'] = UserMultipleChoiceField(queryset=CustomUser.objects.filter(is_active=True).order_by('email'))
        self.fields['assigned_by'] = UserFullnameChoiceField(queryset=CustomUser.objects.filter(is_active=True))
        self.fields['reference_task'].queryset = TaskManager.objects.filter(delete_status=0, task_visibility=1)
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

