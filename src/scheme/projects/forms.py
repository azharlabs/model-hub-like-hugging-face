from scheme.teams.models import Team

from django import forms
from .models import Project


class ProjectEditForm(forms.ModelForm):
    def teams_choices():
        value = []
        team = Team.objects.all()
        for i in team:
            value.append((i, i.title))
        return value


    project_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Project Title', 'class': 'form-control'}))
    team = forms.MultipleChoiceField(choices=teams_choices(), required=True, widget=forms.Select(attrs={'class':'js-select form-select'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    client_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Client Name','class': 'form-control'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}))
    

    class Meta:
        model = Project
        fields = ['project_name', 'team', 'image', 'description', 'client_name']
       
           
          