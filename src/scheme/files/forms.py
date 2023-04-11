from django import forms
from django.forms import ClearableFileInput
from .models import Files



class ScriptFileUploadForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['script_file']
        widgets = {
            'script_file': ClearableFileInput(attrs={'multiple': False}),
        }


