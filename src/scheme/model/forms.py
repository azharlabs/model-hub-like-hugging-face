from django import forms
from django.forms import ClearableFileInput
from .models import Model



class ModelUploadForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['file_name']
        widgets = {
            'file_name': ClearableFileInput(attrs={'multiple': False}),
        }
