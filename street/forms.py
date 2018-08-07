from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Neighbourhood, Business, Post, Profile, Comments

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['bio', 'avatar']

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['topic', 'message', 'image']

class CommentsForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields = ['comment']

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        fields=['name','email_address','description']

class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model=Neighbourhood
        fields=['name','population','location']
