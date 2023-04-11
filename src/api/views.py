import uuid

from django.shortcuts import render, redirect, get_object_or_404

from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

from scheme.product.models import Product
from scheme.teams.models import Team
from scheme.tasks.models import Task
from .models import API, apiLog
from .forms import apiAddForm


@login_required()
def api_home(request):
    team = Team.objects.filter(members__in=[request.user])
    api_list = API.objects.filter(team__in=team).order_by('-created_date')
    
    apilog = apiLog.objects.filter(api__in=api_list)
    amount = 0
    products = []
    for api in apilog:
        amount += api.price
        products.append(api.product)



    print("apilog", apilog)
    
    value = []
    team = Team.objects.all()
    for i in team:
        value.append(i.title)


    context = {
        'api_list':api_list,
        'count':len(api_list),
        'team_list':value,
        'amount':amount,
        'product_count': len(set(products)),
    }
    return render(request, 'api/api_home.html', context)

@login_required()
def add(request):
    
    if request.method == 'POST':
 
        print('post request')
        
        # if form.is_valid():
        print('form valid')
        print("request.POST.get('team')", request.POST.get('team'))
        team = get_object_or_404(Team, title=request.POST.get('team'))
        api = API.objects.create(user=request.user,team=team, api='SK_' + str(uuid.uuid4()).replace('-', ''), active=True)
      
        api.save()

        messages.success(request, 'API added')

        return redirect('api:api_home')

        messages.error(request, 'Please select the proper values')
        return redirect('api:api_home')

    messages.success(request, 'Something went wrong')
    return redirect('api:api_home')

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
            project.team.add(team)
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
def api_detail(request, pk):
    api = get_object_or_404(API, pk=pk)
    team = get_object_or_404(Team, pk=api.team.pk)
    apilog = apiLog.objects.filter(api=api)
    amount = 0
    products = {}
    for api in apilog:
        amount += api.price
        if api.product in products:
            products[api.product.product_name] += amount
        else:
             # Adding the amount to the product.
             products[api.product.product_name] = amount

    if request.user in team.members.all():
        context = {
            'amount':amount,
            'product_count': len(set(products.keys())),
            'products': ','.join(list(products.keys())),
            'product_amount': ','.join(["{:.3f}".format(float(i)) for i in products.values()])

        }
        return render(request, 'api/api_detail.html', context)
    else:
        return redirect('api:api_home')


@login_required()
def delete(request):
    context ={}
    if request.method =="POST":
        print("dict", dict(request.POST), request.POST.getlist('id'))
        for i in request.POST.getlist('id'):
            print("i=============", i)
            obj = get_object_or_404(API, id = i)
            # delete object
            obj.delete()
        return redirect('api:api_home')
 
    return HttpResponse("Something went wrong")