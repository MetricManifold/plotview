from django import forms
from .models import Directory

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['path']
