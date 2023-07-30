from django import forms
from django.core.validators import validate_ipv4_address
from django.core.exceptions import ValidationError

from licenseinfo.models import LicenseInfo, LicenseType, M365License
class LicenseAddForm(forms.ModelForm):
    class Meta:
        model = LicenseInfo
        fields = ('license_name','license_number', 'service_name', 'service_group', 'effective_quantity', 'license_type', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super(LicenseAddForm, self).__init__(*args, **kwargs)

        self.fields['license_type'].queryset = LicenseType.objects.filter(delete_status=False)

class LicenseFilterForm(forms.ModelForm):
    class Meta:
        model = LicenseInfo
        fields = ['license_type']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['license_status'].choices = [(entry['license_status'], entry['license_status']) for entry in LicenseInfo.objects.values('license_status').distinct()]

class LicenseEditForm(forms.ModelForm): 
    def __init__(self,pk,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pk=pk
        self.fields['license_type'].queryset = LicenseType.objects.filter(delete_status=False)

    class Meta:
        model = LicenseInfo
        fields = ('license_name','license_number', 'service_name', 'service_group', 'effective_quantity', 'license_type', 'start_date', 'end_date')

class M365AddForm(forms.ModelForm):
    class Meta:
        model = M365License
        fields = ('user_name','user_id', 'hostname', 'ip_address', 'branch', 'date')
    def clean(self):
            user_name  = self.cleaned_data.get('user_name')
            user_id  = self.cleaned_data.get('user_id')
            hostname  = self.cleaned_data.get('hostname')
            ip_address  = self.cleaned_data.get('ip_address')
            branch  = self.cleaned_data.get('branch')
            date  = self.cleaned_data.get('date')

            if not user_name or not user_id or not hostname or not ip_address or not branch or not date:
                raise ValidationError("Enter all required fields with valid data")

            if ip_address or ip_address == None :
                try:
                    validate_ipv4_address(ip_address)
                except ValidationError:
                    raise ValidationError("Please Enter Valid IP")
            
    # def __init__(self, *args, **kwargs):
    #     super(LicenseAddForm, self).__init__(*args, **kwargs)

    #     self.fields['license_type'].queryset = LicenseType.objects.filter(delete_status=False)

        