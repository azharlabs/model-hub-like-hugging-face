from django.shortcuts import render, redirect, get_object_or_404

from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

from scheme.files.models import Files
from scheme.files.forms import ScriptFileUploadForm
from scheme.product.models import Product
from scheme.teams.models import Team
from scheme.tasks.models import Task
from .models import Project
from .forms import ProjectEditForm


@login_required()
def projects_home(request):
    project_list = Project.objects.filter(author=request.user).order_by('-created_date')
    context = {
        'project_list':project_list,
    }
    return render(request, 'scheme/projects/projects_home.html', context)

@login_required()
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_title = Project.objects.filter(project_name=title, author=request.user)
        project_title_len = []
        for i in project_title:
            project_title_len.append(i)
        print("project_title_len======", len(project_title_len))

        if title and len(project_title_len) == 0:
            project = Project.objects.create(project_name=title, author=request.user, description=description)
      
            project.save()

            return HttpResponse('Project added')
        return HttpResponse('Project title must be unique')
    
    return HttpResponse('Something went wrong')

@login_required()
def edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectEditForm(instance =project)
    if request.method == 'POST':
        form = ProjectEditForm(request.POST,request.FILES, instance =project)
        team = get_object_or_404(Team, title=request.POST.get('team'))
        print("request team======", request.POST.get('team',''))
        
        if form.is_valid():
            project = form.save(commit=False)
            project.team = team
            print("project.team=================",project.team)

            project.save()
            print("You successfully updated the Project")
            return redirect('dashboard:projects:project_detail', pk)
        else:
            print(form.errors)
            print('form not valid')
    context = {
            'form':form
        }


    return render(request, 'scheme/projects/edit.html', context)

@login_required()
def project_detail(request, pk):
    
    project = get_object_or_404(Project, pk=pk)
    product = Product.objects.filter(project=project)


    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)

    tasks = Task.objects.filter(project=project)

    context = {
        'project':project,
        'product':product,
        'tasks':tasks,
        'tasks_todo':tasks_todo,
        'tasks_done':tasks_done,
        'team_choices': project.team,
    }
    return render(request, 'scheme/projects/project_detail.html', context)



@login_required()
def delete(request):
    context ={}
    if request.method =="POST":
        print("dict", dict(request.POST), request.POST.getlist('id'))
        for i in request.POST.getlist('id'):
            print("i=============", i)
            obj = get_object_or_404(Project, id = i)
            # delete object
            obj.delete()
        return redirect('dashboard:projects:projects_home')
 
    return HttpResponse("Something went wrong")


@login_required()
def projects_files(request, pk):
    project = get_object_or_404(Project, pk=pk)
    files = Files.objects.filter(project=project)
    context = {
        'files':files,
        'project':project,
        'form':ScriptFileUploadForm,
    }
    return render(request, 'scheme/projects/projects_files.html', context)