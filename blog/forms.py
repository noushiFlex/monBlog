from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    
class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username*'
        })
    )
    email = forms.EmailField(
        max_length=50, 
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email*'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe*'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer mot de passe*'
        })
    )
    
    class Meta:
        model = User  
        fields = ['username', 'email', 'password1', 'password2']
