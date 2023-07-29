from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form
from django.contrib.auth.hashers import make_password
 
  
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'label': 'username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'label': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'label': 'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'label': 'password2'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class CrudUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'label': 'username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'label': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'label': 'password1'}))

    class Meta:
        model = User
        fields = ['username','email','password1']

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(is_active=True).exists():
            raise ValidationError('Username already exists.')
        return username
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            password = make_password(password)
        return password


    




  