from django.contrib.auth import get_user_model
from django.core.validators import validate_ipv4_address
from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError


from .models import *

# class ServiceWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "service_name__icontains",
#     ]

class ServerRackInfoAddForm(forms.ModelForm):
    class Meta:
        model = ServerRackInfo
        fields = ('location','rack', 'loc_in_rack', 'form_factor')

class ServerAddForm(forms.ModelForm):
    class Meta:
        model = PhysicalServer
        exclude = ('update_by','update_time')

    def __init__(self, *args, **kwargs):
        super(ServerAddForm, self).__init__(*args, **kwargs)
        all_physical_server = PhysicalServer.objects.filter(delete_status=False)
        all_vm_server = VirtualServer.objects.filter(delete_status=False)
        all_service_list=[]
        for i in all_physical_server:
            if i.service_name.filter(delete_status=False):
                for j in i.service_name.filter(delete_status=False):
                    all_service_list.append(j)
        for i in all_vm_server:
            if i.service_name.filter(delete_status=False):
                for j in i.service_name.filter(delete_status=False):
                    all_service_list.append(j)
                    
        self.fields['service_name'].queryset = RunningServices.objects.filter(delete_status=False).exclude(service_name__in=all_service_list)
        self.fields['os_type'].queryset = OsType.objects.filter(delete_status=False)
        self.fields['os_version'].queryset = OsVersion.objects.filter(delete_status=False)
        self.fields['zone'].queryset = Zone.objects.filter(delete_status=False)
        self.fields['project'].queryset = Project.objects.filter(delete_status=False)

    def clean(self):
        
        idrac_ip = self.cleaned_data.get('idrac_ip')
        primary_ip = self.cleaned_data.get('primary_ip')
        public_ip = self.cleaned_data.get('public_ip')
        server_name = self.cleaned_data.get('server_name')
        secondary_ip = self.cleaned_data.get('secondary_ip')
        service_tag = self.cleaned_data.get('service_tag')
        asset_code = self.cleaned_data.get('asset_code')

        if server_name:
            if PhysicalServer.objects.filter(server_name=server_name):
                raise ValidationError("Server with same name exists")

        if primary_ip:
            if PhysicalServer.objects.filter(primary_ip=primary_ip):
                raise ValidationError("Server with same Primary IP exists")
        if public_ip:
            if PhysicalServer.objects.filter(public_ip=public_ip):
                raise ValidationError("Server with same Public IP exists")
        if secondary_ip:
            if PhysicalServer.objects.filter(secondary_ip=secondary_ip):
                raise ValidationError("Server with same Secondary IP exists")
        if service_tag:
            if PhysicalServer.objects.filter(service_tag=service_tag):
                raise ValidationError("Server with same Service Tag exists")     
        if asset_code:
            if PhysicalServer.objects.filter(asset_code=asset_code):
                raise ValidationError("Server with same Asset Code exists")     
      

        if idrac_ip or idrac_ip == None :
            try:
                validate_ipv4_address(idrac_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid iDRAC IP")

        if primary_ip or primary_ip == None :
            try:
                
                validate_ipv4_address(primary_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Primary IP")
        

        if public_ip or public_ip == None :
            try:
                validate_ipv4_address(public_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Public IP")   

class ServerEditForm(forms.ModelForm):
    def __init__(self, pk, *args, **kwargs):
        super(ServerEditForm, self).__init__(*args, **kwargs)
        all_physical_server = PhysicalServer.objects.filter(delete_status=False).exclude(pk=pk)
        all_vm_server = VirtualServer.objects.filter(delete_status=False)

        all_service_list=[]
        for physical_server in all_physical_server:
            if physical_server.service_name.filter(delete_status=False):
                for service in physical_server.service_name.filter(delete_status=False):
                    all_service_list.append(service)
        for vm in all_vm_server:
            if vm.service_name.filter(delete_status=False):
                for service in vm.service_name.filter(delete_status=False):
                    all_service_list.append(service)
        self.fields['service_name'].queryset = RunningServices.objects.filter(delete_status=False).exclude(service_name__in=all_service_list)

        self.fields['server_name'].widget.attrs['readonly'] = True
        self.fields['os_type'].queryset = OsType.objects.filter(delete_status=False)
        self.fields['os_version'].queryset = OsVersion.objects.filter(delete_status=False)
        self.fields['zone'].queryset = Zone.objects.filter(delete_status=False)
        self.fields['project'].queryset = Project.objects.filter(delete_status=False)

    class Meta:
        model = PhysicalServer
        exclude = ('update_by','update_time')

    def clean(self):
        cleaned_data = super().clean()



        idrac_ip = cleaned_data.get('idrac_ip')
        primary_ip = cleaned_data.get('primary_ip')
        public_ip = cleaned_data.get('public_ip')
        if idrac_ip or idrac_ip == None :
            try:
                validate_ipv4_address(idrac_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid iDRAC IP")

        if primary_ip or primary_ip == None :
            try:
                validate_ipv4_address(primary_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Primary IP")
        
        if public_ip or public_ip == None :
            try:
                validate_ipv4_address(public_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Public IP") 

class ServerRackInfoEditForm(forms.ModelForm):
    class Meta:
        model = ServerRackInfo
        fields = ('location','rack', 'loc_in_rack', 'form_factor')

class VMAddForm(forms.ModelForm):
    class Meta:
        model = VirtualServer
        exclude = ('update_by','update_time')

    def __init__(self, *args, **kwargs):
        super(VMAddForm, self).__init__(*args, **kwargs)

        all_physical_server = PhysicalServer.objects.filter(delete_status=False)
        all_vm_server = VirtualServer.objects.filter(delete_status=False)
        all_service_list=[]
        for physical_server in all_physical_server:
            if physical_server.service_name.filter(delete_status=False):
                for service in physical_server.service_name.filter(delete_status=False):
                    all_service_list.append(service)
        for vm in all_vm_server:
            if vm.service_name.filter(delete_status=False):
                for service in vm.service_name.filter(delete_status=False):
                    all_service_list.append(service)
        self.fields['service_name'].queryset = RunningServices.objects.filter(delete_status=False).exclude(service_name__in=all_service_list)
        self.fields['os_type'].queryset = OsType.objects.filter(delete_status=False)
        self.fields['os_version'].queryset = OsVersion.objects.filter(delete_status=False)
        self.fields['zone'].queryset = Zone.objects.filter(delete_status=False)

    def clean(self):
        primary_ip = self.cleaned_data.get('primary_ip')
        public_ip = self.cleaned_data.get('public_ip')

        if primary_ip or primary_ip == None :
            try:
                validate_ipv4_address(primary_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Primary IP")
        

        if public_ip or public_ip == None :
            try:
                validate_ipv4_address(public_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Public IP") 

class VMEditForm(forms.ModelForm):
    def __init__(self, pk, *args, **kwargs):

        super(VMEditForm, self).__init__(*args, **kwargs)
        all_physical_server = PhysicalServer.objects.filter(delete_status=False)
        all_vm_server = VirtualServer.objects.filter(delete_status=False).exclude(pk=pk)

        all_service_list=[]
        for physical_server in all_physical_server:
            if physical_server.service_name.filter(delete_status=False):
                for service in physical_server.service_name.filter(delete_status=False):
                    all_service_list.append(service)
        for vm in all_vm_server:
            if vm.service_name.filter(delete_status=False):
                for service in vm.service_name.filter(delete_status=False):
                    all_service_list.append(service)
        self.fields['service_name'].queryset = RunningServices.objects.filter(delete_status=False).exclude(service_name__in=all_service_list)

        self.fields['server_name'].widget.attrs['readonly'] = True
        self.fields['os_type'].queryset = OsType.objects.filter(delete_status=False)
        self.fields['os_version'].queryset = OsVersion.objects.filter(delete_status=False)
        self.fields['zone'].queryset = Zone.objects.filter(delete_status=False)

    class Meta:
        model = VirtualServer
        exclude = ('update_by','update_time')

    def clean(self):
        cleaned_data = super().clean()

        primary_ip = cleaned_data.get('primary_ip')
        public_ip = cleaned_data.get('public_ip')

        if primary_ip or primary_ip == None :
            try:
                validate_ipv4_address(primary_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Primary IP")
        

        if public_ip or public_ip == None :
            try:
                validate_ipv4_address(public_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid Public IP") 
                 
class ServiceAddForm(forms.ModelForm):
    class Meta:
        model = RunningServices
        exclude = ('update_by','update_time', 'delete_status', 'deleted_by', 'delete_time')

    def clean(self):
        service_name = self.cleaned_data.get('service_name')
        service_ip = self.cleaned_data.get('service_ip')
        # print(self.cleaned_data.get('service_log_loc'))

        service_exist = RunningServices.objects.filter(service_name=service_name)
        if service_exist:
            raise ValidationError(f'Service with name "{service_name}" alredy exists.')
        if service_ip:
            try:
                validate_ipv4_address(service_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid IP")
        if self.cleaned_data.get('monitoring_enabled') == 1 and self.cleaned_data.get('service_log_loc') == None:
            raise ValidationError(f'Please enter log directory name when monitor is enabled')

class ServiceAddFormModal(forms.ModelForm):
    class Meta:
        model = RunningServices
        exclude = ('update_by','update_time', 'delete_status', 'deleted_by', 'delete_time')

    # def clean(self):
    #     service_name = self.cleaned_data.get('service_name')
    #     service_ip = self.cleaned_data.get('service_ip')

class ServiceEditForm(forms.ModelForm): 
    def __init__(self,pk,*args,**kwargs):
          super().__init__(*args,**kwargs)
          self.pk=pk
    class Meta:
        model = RunningServices
        exclude = ('update_by','update_time', 'delete_status', 'deleted_by', 'delete_time')
    def clean(self):
        service_name = self.cleaned_data.get('service_name')
        service_ip = self.cleaned_data.get('service_ip')
        service_exist = RunningServices.objects.filter(~Q(pk = self.pk), service_name=service_name)
        if service_exist:
            raise ValidationError(f'Service with name "{service_name}" alredy exists.')
        if service_ip:
            try:
                validate_ipv4_address(service_ip)
            except ValidationError:
                raise ValidationError("Please Enter Valid IP")

        # if self.cleaned_data.get('monitoring_enabled') == 1 and self.cleaned_data.get('service_log_loc') == None:
        #     raise ValidationError(f'Please enter log directory name when monitor is enabled')





