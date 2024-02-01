from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from .models import *

class AddIncidenceForm(forms.ModelForm):
    class Meta:
        model = Incidence
        fields = [
            'title',
            'urgency',
            'impact',
            'status',
            'related_kb',
            'reported_by',
            'assigned_to',
            'triggered_time',
            'responsed_at',
            'resolved_by',
            'resolved_at'
        ]

    def clean(self):
        
        current_time = timezone.now()
        # current_time = datetime.datetime.now()

        title = self.cleaned_data.get('title')
        urgency = self.cleaned_data.get('urgency')
        impact = self.cleaned_data.get('impact')
        status = self.cleaned_data.get('status')
        related_kb = self.cleaned_data.get('related_kb')
        reported_by = self.cleaned_data.get('reported_by')
        triggered_time = self.cleaned_data.get('triggered_time')
        responsed_at = self.cleaned_data.get('responsed_at')
        resolved_by = self.cleaned_data.get('resolved_by')
        resolved_at = self.cleaned_data.get('resolved_at')
        # print(type(current_time), '    ', type(triggered_time))
        if current_time < triggered_time or current_time < responsed_at:
            raise ValidationError("Time must not be greater than current time.")
        if resolved_at:
            if current_time < resolved_at:
                raise ValidationError("Time must not be greater than current time.")
        
        if not title or not urgency or not impact or not reported_by or not triggered_time or not responsed_at:
            raise ValidationError("Please Enter required fileds")
        if not related_kb:
            raise ValidationError("Please Enter Related KB about incidence description and resolution")        
        if status == 3 and not resolved_by:
            raise ValidationError("Please Select Resolver(s)")
        if status == 3 and not resolved_at:
            raise ValidationError("Please Select Resolve Time")

# class AddResolutionForm(forms.ModelForm):
#     class Meta:
#         model = Resolution
#         fields = [
#             'resolution',
#             'related_kb',
#             'resolved_by',
#             'resolved_at',
#         ]

#     def clean(self):
        
#         resolution = self.cleaned_data.get('resolution')
#         related_kb = self.cleaned_data.get('related_kb')
#         resolved_by = self.cleaned_data.get('resolved_by')
#         resolved_at = self.cleaned_data.get('resolved_at')

#         if not resolution or not related_kb:
#             raise ValidationError("Please Enter Resolution Procedure or Related Knowlage")
        
#         if not resolved_by:
#             raise ValidationError("Please Select Resolver(s)")
#         if not resolved_at:
#             raise ValidationError("Please Select Resolve Time")