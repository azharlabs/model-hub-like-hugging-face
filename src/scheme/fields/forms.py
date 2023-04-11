from django import forms
from .models import Fields


class fieldForm(forms.ModelForm):
    class Meta:
        model = Fields
        fields = ('field_name','field_type', 'description')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(fieldForm, self).__init__(*args, **kwargs)
        self.fields['field_name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control', }
        self.fields['field_type'].widget.attrs = {'class':'form-control', }
        self.fields['description'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}