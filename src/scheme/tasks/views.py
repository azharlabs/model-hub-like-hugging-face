from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


from scheme.projects.models import Project
from scheme.teams.models import Team
from .models import Task


@login_required()
def add(request):
    if request.method == 'POST':
        print(dict(request.POST))
        title = request.POST.get('title')
        selected_team = request.POST.get('selected_team')
        selected_project = request.POST.get('selected_project')

        team = get_object_or_404(Team,title=selected_team)
        project = get_object_or_404(Project,pk=selected_project)

        if title:
            task = Task.objects.create(team=team, project=project, created_by=request.user, title=title,status='Todo' )

            messages.info(request, 'The task was added!')

            return HttpResponse('tasks added')
    
    context = {

    }
    return HttpResponse('Something Wrong')



