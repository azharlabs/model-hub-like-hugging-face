from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget


choices_list = (
('draft', 'Draft'),
('published', 'Published')
)
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','tags', 'status', 'body' )
        widgets = {
            'title':forms.TextInput(attrs={'class':"form-control"}),
            'body':forms.Textarea( attrs={'class':"form-control"}),
            'status':forms.Select(choices=choices_list, attrs={'class':"form-control"}),
            'tags':TagWidget( attrs={'class':"form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control', }
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}