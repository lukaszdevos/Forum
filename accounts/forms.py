from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from accounts.models import Profile




class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
        
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email' )



class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('description','city','website','profile_img')
        
        
class PasswordResetForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('__all__')
        
class SetPasswordForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('__all__')
        


