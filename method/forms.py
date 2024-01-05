from django import forms
from .models import JobUser


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    verification_method = forms.ChoiceField(
        choices=JobUser.VERIFICATION_TYPE,
        widget=forms.RadioSelect
    )
    

    class Meta:
        model = JobUser
        fields = ('phone_number', 'password', 'verification_method')

        
class UserLoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)