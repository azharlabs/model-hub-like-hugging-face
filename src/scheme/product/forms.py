from scheme.teams.models import Team

from django import forms
from .models import Product, ProductComment

STATUS_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private')
    )
class ProductEditForm(forms.ModelForm):
    def teams_choices():
        value = []
        team = Team.objects.all()
        for i in team:
            value.append((i, i.title))
        return value


    product_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Project Title', 'class': 'form-control'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    banner_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    status = forms.Select(choices=STATUS_CHOICES, attrs={'class':"form-control"}),
    index = forms.CheckboxInput(attrs={'class':"form-control"})
    price_per_request = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '0.05', 'class': 'form-control'}))

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}))
    # manual = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'User Manual', 'class': 'form-control'}))
    

    class Meta:
        model = Product
        fields = ['product_name', 'profile_pic', 'banner_pic', 'status','index', 'price_per_request', 'description', 'manual']
       
           
class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('body',)
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(ProductCommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}