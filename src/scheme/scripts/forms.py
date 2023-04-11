from django import forms
from .models import Scripts, ScriptComment


class ScriptscriptEditForm(forms.ModelForm):
    class Meta:
        model = Scripts
        fields = ['script_code']
        widgets = {
            'script_code': forms.HiddenInput( attrs={'class':"form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = ScriptComment
        fields = ('body',)
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}