from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from prueba.models import Cuenta , UserCreate , Authenti , App
from django.utils.html import strip_tags
from django.forms import ModelForm

class UserCreateForm (ModelForm):
	class Meta:
		model = UserCreate
		fields = ['email', 'first_name', 'username','password1','password2']
		widgets = {'password1': forms.PasswordInput(),'password2': forms.PasswordInput(),'email':forms.TextInput(attrs={'placeholder': 'Email'}),'first_name':forms.TextInput(attrs={'placeholder': 'LinkedIn'}),'username':forms.TextInput(attrs={'placeholder': 'Username/Twitter'}),'password1':forms.PasswordInput(attrs={'placeholder': 'Password'}),'password2':forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'})}
		

class AuthenticateForm(ModelForm):
	class Meta:
		model = Authenti
		fields = ['username', 'password']
		widgets = {'password': forms.PasswordInput(),'username':forms.TextInput(attrs={'placeholder': 'Nickname/Username'}),'password':forms.PasswordInput(attrs={'placeholder': 'Password'})}
		
class AppForm(ModelForm):
	class Meta:
		model = App
		fields = ['content']

	
	

	
	
	