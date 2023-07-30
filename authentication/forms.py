from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Profile
#from django.contrib.auth.models import User

class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']



class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    #disabled_fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
        # for field in self.disabled_fields:
        #     self.fields[field].disabled = True
        self.fields['email'].disabled = True
    
    class Meta:
        model = User
        fields = ['email', 'first_name','last_name']
        


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','designation','bio']
        widgets = {
            'dob': forms.DateTimeInput(attrs={'type': 'date'}),
        }

