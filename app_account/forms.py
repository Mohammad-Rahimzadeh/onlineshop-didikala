from django import forms
from django.contrib.auth import get_user_model , password_validation
from django.contrib.auth.forms import UserChangeForm
from app_account.models import Profile , Address


User = get_user_model()


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255 , required=True)
    last_name = forms.CharField(max_length=255 , required=True)
    username = forms.CharField(max_length=255 , required=True)
    email = forms.EmailField(max_length=255, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('phone_number',)
        
        

class editProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number' , 'natural_id' , 'card_no' , 'get_newsletter' , 'image']



class editUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['first_name' , 'last_name' , 'email']
    password=None


class addressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['state' , 'city' , 'postal_code' , 'description']



class changePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())