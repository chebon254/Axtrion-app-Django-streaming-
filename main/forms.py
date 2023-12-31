from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class ImageWidget(forms.ClearableFileInput):
#     template_name = 'registration/custom_image_widget.html'

#     def value_from_datadict(self, data, files, name):
#         upload = super().value_from_datadict(data, files, name)
#         clear = forms.CheckboxInput().value_from_datadict(data, files, name + '-clear')

#         if forms.CheckboxInput().value_from_datadict(data, files, name + '-clear'):
#             return False

#         return upload

class UserProfileForm(forms.ModelForm):
    # image = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = UserProfile
        fields = ['image', 'bio']
        
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file', 'custom_thumbnail']

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']