from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from scheme.scripts.models import Scripts
from .models import Fields
from .forms import fieldForm



@login_required()
def fields_home(request):
    context = {

    }
    return render(request, 'scheme/fields/fields_home.html', context)


@login_required()
def addscriptfield_form(request):
    form = fieldForm()
    context = {
        'form':form,
    }
    return render(request, "includes/fields/form.html", context)


@login_required()
def create_fields(request, pk):
    script = get_object_or_404(Scripts, pk=pk)
    form = fieldForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            field = form.save(commit=False)
            field.author = request.user
            field.scripts = script

            field.save()
          
        
    fields = Fields.objects.filter(scripts=script)   
    context = {
        'fields':fields,
    }

    return render(request, 'scheme/fields/list.html', context)




@login_required()
def field_list(request, pk):
    script = get_object_or_404(Scripts, pk=pk)
    fields = Fields.objects.filter(scripts=script)
    context = {
        'fields':fields,
    }
    return render(request, 'scheme/fields/list.html', context)

@login_required()
def delete(request, pk):

    obj = get_object_or_404(Fields, pk=pk)
    script = obj.scripts
    obj.delete()

    fields = Fields.objects.filter(scripts=script)
    context = {
        'fields':fields,
    }

    return render(request, 'scheme/fields/list.html', context)