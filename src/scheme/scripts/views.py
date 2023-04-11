import joblib

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path
from django.core.files import File

from scheme.product.models import Product
from scheme.fields.models import Fields
from .models import Scripts, UpdateScriptInfo, ScriptComment
from .forms import ScriptscriptEditForm, CommentForm
from scheme.fields.forms import fieldForm
from scheme.endpoints.models import endPoint
from scheme.model.models import Model


@login_required()
def scripts_home(request):
    context = {}
    return render(request, 'scheme/scripts/scripts_home.html', context)


@login_required()
def add(request, pk):
    print('request.post==================', request.FILES)
    product = get_object_or_404(Product, pk=pk)
    product_len = Scripts.objects.filter(product=product)
    print("product_len========", len(product_len))
    if len(product_len) == 0:            

        script_instance = Scripts.objects.create(author=request.user, product=product)
        script_pk = script_instance.pk
        script_instance.save()
        return redirect('dashboard:scripts:script_detail', script_pk)
                    
    else:
        script_pk = get_object_or_404(Scripts, product=product).pk
        return redirect('dashboard:scripts:script_detail', script_pk)


@login_required()
def script_detail(request, pk):
    script_code = get_object_or_404(Scripts, pk=pk).script_code
    scripts = get_object_or_404(Scripts, pk=pk)
    fields = Fields.objects.filter(scripts=scripts)
    product = get_object_or_404(Scripts, pk=pk).product
    print("product==========",product)
    endpoint = endPoint.objects.filter(product=product)
    print(endpoint)
    if len(endpoint) == 0:
        with open('endpoint.py', 'w') as f:
            f.write('')
        endpoint_instance = endPoint.objects.create(product=scripts.product)
        endpoint_instance.save()

    field_form = fieldForm()

    comment_form = CommentForm(request.POST)
    
    context = {
        'contents':script_code,
        'scripts':scripts,
        'comment_form':comment_form,
        'field_form':field_form,
        'fields':fields,
    }
    return render(request, 'scheme/scripts/script_detail.html', context)


@login_required()
def edit(request, pk):

    scripts = get_object_or_404(Scripts, pk=pk)
    form = ScriptscriptEditForm(request.POST or None,instance=scripts)
    fields = Fields.objects.filter(scripts=scripts)
    field_tile =  [i.field_name for i in fields]
    excute_function = 'print(endpoint(' + ','.join(field_tile) + '))'
    script_code = get_object_or_404(Scripts, pk=pk).script_code
    model = get_object_or_404(Model, product=scripts.product).file_name
    model_file_path = str(settings.MEDIA_ROOT)+'/' + str(model)

    endpoint = get_object_or_404(endPoint, product=scripts.product) 
    print(endpoint)
        

    if endpoint:
        with open('endpoint.py', 'w') as f:
            f.write('import sys\n')
            f.write('import ast\n\n\n')
           

            f.write('try:\n')
            start = 1
            for i in field_tile:
                f.write(f'    {i} = ast.literal_eval(sys.argv[{start}])\n')
                start +=1
            f.write('except:\n')
            f.write('    sys.exit("pass all the arguments")\n\n\n')
            f.write(f'model = {joblib.load(model_file_path)}\n\n')
            f.write(script_code)
            f.write('\n\n\n')
            
            f.write(excute_function)
            
        path = Path('endpoint.py')
        with path.open(mode='rb') as f:
            endpoint.endpoint_file = File(f, name='endpoint.py') # open(str(settings.MEDIA_ROOT)+'/' + str(scripts.script_file)) as f:
            print(endpoint.endpoint_file)
            endpoint.save()
            

    context = {
        'form':form,
        'script_code':script_code,
        'scripts':scripts,
    }
    if form.is_valid():
        files = form.save(commit=False)
        if endpoint:
            with open('endpoint.py', 'w') as f:
                f.write('import sys\n')
                f.write('import ast\n\n\n')
               
                f.write('try:\n')
                start = 1
                for i in field_tile:
                    f.write(f'    {i} = ast.literal_eval(sys.argv[{start}])\n')
                    start +=1
                f.write('except:\n')
                f.write('    sys.exit("pass all the arguments")\n\n\n')
                f.write(f'model = {joblib.load(model_file_path)}\n\n')
                f.write(files.script_code)
                f.write('\n\n\n')
                
                f.write(excute_function)
                
            path = Path('endpoint.py')
            with path.open(mode='rb') as f:
                endpoint.endpoint_file = File(f, name='endpoint.py') # open(str(settings.MEDIA_ROOT)+'/' + str(scripts.script_file)) as f:
                print(endpoint.endpoint_file)
                endpoint.save()
 
        files.save()

        UpdateScriptInfo.objects.create(scripts=files, updated_author=request.user)
        print("You successfully updated the script")
        return redirect('dashboard:scripts:script_detail', pk)
    else:
        print(form.errors)
        print('form not valid')


    return render(request, 'scheme/scripts/edit.html', context)

@login_required()
def create_comments(request, pk):
    script = get_object_or_404(Scripts, pk=pk)
    form = CommentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            script_comment = form.save(commit=False)
            script_comment.name = request.user.username
            script_comment.email = request.user.email
            script_comment.script = script

            script_comment.save()
          
        
    comments = script.comments.filter(active=True)

    print(comments)
    
    context = {
        'comments':comments,
        'scripts':script,
    }
    return render(request, 'scheme/scripts/comment_list.html', context)


@login_required()
def comment_list(request, pk):
    script = get_object_or_404(Scripts, pk=pk)
    comments = script.comments.filter(active=True)
    context = {
        'comments':comments,
    }
    return render(request, 'scheme/scripts/comment_list.html', context)

# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)

            reply.name = request.user.username
            reply.email = request.user.email
            
    
            reply.script = Scripts(pk=post_id)
            reply.parent = ScriptComment(pk=parent_id)
           
            reply.save()

           

    script = get_object_or_404(Scripts, pk=post_id)      
    comments = script.comments.filter(active=True)
    context = {
        'comments':comments,
        'scripts':script,
    }
    return render(request, 'scheme/scripts/comment_list.html', context)

