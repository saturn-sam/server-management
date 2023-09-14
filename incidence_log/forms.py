from django import forms

from .models import *

class AddIncidenceForm(forms.ModelForm):
    class Meta:
        model = Incidence
        fields = [
            'title',
            'urgency',
            'impact',
            'status',
            'incidence_description',
            'reported_by',
            'assigned_to',
            'triggered_time',
            'responsed_at'
        ]