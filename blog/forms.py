from django import forms
from .models import Profile, Posts

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content']
