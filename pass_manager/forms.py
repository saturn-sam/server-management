from django.contrib.auth import get_user_model
from django.core.validators import validate_ipv4_address
from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
import hashlib
from django.conf import settings
from authentication.models import CustomUser
from django.shortcuts import get_object_or_404
from .models import *

class MasterKeyAddForm(forms.Form):
    master_key_name = forms.CharField(label='Master Key Title', required = True,  help_text="Enter Title of Master Key.")
    master_key = forms.CharField(label='Master Key', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key")
    master_key_confirm = forms.CharField(label='Confirm Master Key', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key again")
    
    

    def clean(self):

        if self.cleaned_data.get('master_key') != self.cleaned_data.get('master_key_confirm'):
            raise ValidationError("Password didn't match!")

        if len(self.cleaned_data.get('master_key')) < 4:
            raise ValidationError('Minimum Length of Password: 4')

        mp_ins = Secret.objects.filter(master_key_name=self.cleaned_data.get('master_key_name'))

        if mp_ins:
            raise ValidationError('Master key with Same Title Exist!')
        
class MasterKeyChangeForm(forms.Form):
    master_key_name = forms.ChoiceField()
    current_master_key = forms.CharField(label='Current Master Key', required = True, widget=forms.PasswordInput(), help_text="Enter Current Master Key")
    master_key = forms.CharField(label='New Master Key', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key")
    master_key_confirm = forms.CharField(label='Confirm Master Key', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key again")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MasterKeyChangeForm, self).__init__(*args, **kwargs)
        
        master_keys = Secret.objects.filter(user_id=self.user)
        self.fields['master_key_name'].choices = [(master_key.pk, master_key.master_key_name) for master_key in master_keys]

    def clean(self):
        current_master_key = self.cleaned_data.get('current_master_key')
        current_hashed_mp = hashlib.sha256(current_master_key.encode()).hexdigest()
        master_key_id = self.cleaned_data.get('master_key_name')

        # mp_ins = Secret.objects.filter(user_id=self.user, masterkey_hash=current_hashed_mp)
        mp_ins = Secret.objects.filter(user_id=self.user, masterkey_hash=current_hashed_mp, pk=master_key_id)
        if not mp_ins:
            raise ValidationError("Current Master Key didn't match!")

        if self.cleaned_data.get('master_key') != self.cleaned_data.get('master_key_confirm'):
            raise ValidationError("New Master Key didn't match!")

        if len(self.cleaned_data.get('master_key')) < 4:
            raise ValidationError('Minimum Length of Master Key: 4')

class AddEntryForm(forms.Form):
    master_key_name = forms.ChoiceField(label='Master Key')
    master_key = forms.CharField(label='Master Key', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key")
    site_server_name = forms.CharField(label='Site/Server Name', required = True,  help_text="Enter Title of Master Key.")
    ip_or_url = forms.CharField(label='Site/Server IP/URL', required = True,  help_text="Enter Title of Master Key.")
    username = forms.CharField(label='Login Username', required = True,  help_text="Enter Title of Master Key.")
    password = forms.CharField(label='Password', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key again")
    remark = forms.CharField(label='Note', required = False, widget=forms.Textarea())


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddEntryForm, self).__init__(*args, **kwargs)
        self.fields['remark'].widget.attrs['rows'] = 3
        
        master_keys = Secret.objects.filter(user_id=self.user)
        self.fields['master_key_name'].choices = [(master_key.pk, master_key.master_key_name) for master_key in master_keys]
    
    def clean(self):
        master_key = self.cleaned_data.get('master_key')
        hashed_mp = hashlib.sha256(master_key.encode()).hexdigest()
        master_key_id = self.cleaned_data.get('master_key_name')
        mp_ins = Secret.objects.filter(user_id=self.user, masterkey_hash=hashed_mp, pk=master_key_id)

        site_server_name = self.cleaned_data.get('site_server_name')
        ip_or_url = self.cleaned_data.get('ip_or_url')

        pass_ins = Passwd.objects.filter(site_server_name=site_server_name, ip_or_url=ip_or_url)
        if pass_ins:
            raise ValidationError("Entry with Same 'Site/Server Name' and 'Site/Server IP/URL' Exist.")

        if not mp_ins:
            raise ValidationError("Provide Currect Master Key!")

class EditEntryForm(forms.Form):
    old_master_key_name = forms.CharField(label='Current Master Key Title')
    old_master_key = forms.CharField(label='Current Master Key', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key")
    change_master_key = forms.BooleanField(label='Change Master Key', required = False)
    new_master_key_name = forms.ChoiceField(label='New Master Key Title', required = False)
    new_master_key = forms.CharField(label='New Master Key', required = False, widget=forms.PasswordInput(), help_text="Enter Master Key")
    site_server_name = forms.CharField(label='Site/Server Name', required = True,  help_text="Enter Title of Master Key.")
    ip_or_url = forms.CharField(label='Site/Server IP/URL', required = True,  help_text="Enter Title of Master Key.")
    username = forms.CharField(label='Login Username', required = True,  help_text="Enter Title of Master Key.")
    password = forms.CharField(label='Password', required = True, widget=forms.PasswordInput(), help_text="Enter Master Key again")
    remark = forms.CharField(label='Note', required = False, widget=forms.Textarea())


    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.user = kwargs.pop('user')
        self.pass_inst = kwargs.pop('pass_inst')

        super(EditEntryForm, self).__init__(*args, **kwargs)
        self.fields['remark'].widget.attrs['rows'] = 3
        self.fields['old_master_key_name'].widget.attrs['readonly'] = True

        master_keys = Secret.objects.filter(user_id=self.user)
        self.fields['new_master_key_name'].choices = [(master_key.pk, master_key.master_key_name) for master_key in master_keys]
    
    def clean(self):

        old_master_key = self.cleaned_data.get('old_master_key')
        hashed_old_mp = hashlib.sha256(old_master_key.encode()).hexdigest()
        old_master_key_id = self.cleaned_data.get('old_master_key_name')
        old_mp_ins = Secret.objects.filter(user_id=self.user, masterkey_hash=hashed_old_mp, master_key_name=old_master_key_id)

        if not old_mp_ins:
            raise ValidationError("Provide Currect Current Master Key!")

        change_master_key = self.cleaned_data.get('change_master_key')
        new_master_key = self.cleaned_data.get('new_master_key')

        if change_master_key:
            if not new_master_key:
                raise ValidationError("Select and Enter New Master Key")
            
            
            new_master_key_id = self.cleaned_data.get('new_master_key_id')

            new_hashed_mp = hashlib.sha256(new_master_key.encode()).hexdigest()
            new_mp_ins = Secret.objects.filter(user_id=self.user, masterkey_hash=new_hashed_mp, pk=new_master_key_id)
            if not new_mp_ins:
                raise ValidationError("Provide Currect New Master Key!")

        site_server_name = self.cleaned_data.get('site_server_name')
        ip_or_url = self.cleaned_data.get('ip_or_url')

        pass_ins = Passwd.objects.filter(site_server_name=site_server_name, ip_or_url=ip_or_url).exclude(user_id=self.user)
        
        if pass_ins:
            raise ValidationError("Entry with Same 'Site/Server Name' and 'Site/Server IP/URL' Exist.")







