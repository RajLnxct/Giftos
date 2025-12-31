from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class RegisterUser(UserCreationForm):
    name = forms.CharField(required=True,label='Username',widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter your Username'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder':'Enter your Email'}))
    password1 = forms.CharField(required=True,label='Password',widget=forms.TextInput(
        attrs={'class':'form-control','type':'password','placeholder':'Enter your Password'}))
    password2 = forms.CharField(required=True,label='Confirm Password',widget=forms.TextInput(
        attrs={'class':'form-control','type':'password','placeholder':'Enter your Confirm Password'}))

    class Meta:
        model = user
        fields = ['name', 'email', 'password1', 'password2']

    def __str__(self):
        return self.name

