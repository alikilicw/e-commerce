from django import forms 
from .models import CustomUser

class CustomUserChangeImages(forms.ModelForm):
    class Meta: 
        model = CustomUser
        fields = ('profile_image', 'cover_image')