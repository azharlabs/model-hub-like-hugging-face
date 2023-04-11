from django import forms
from .models import pandasCode


class pandasScriptEditForm(forms.ModelForm):
    class Meta:
        model = pandasCode
        fields = ['pandas_code']
        widgets = {
            'pandas_code': forms.HiddenInput( attrs={'class':"form-control"}),
        }