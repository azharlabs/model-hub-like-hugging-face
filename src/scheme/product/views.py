import uuid
import requests
from datetime import datetime, timedelta

from tracking_analyzer.models import Tracker
from taggit.models import Tag
from taggit.models import TaggedItem

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import connections

from scheme.files.models import Files
from scheme.projects.models import Project
from scheme.model.models import Model
from scheme.files.forms import ScriptFileUploadForm
from scheme.model.forms import ModelUploadForm
from scheme.endpoints.models import endPoint
from scheme.fields.models import Fields
from scheme.scripts.models import Scripts
from scheme.teams.models import Team
from api.models import apiplayLog
from .forms import ProductEditForm, ProductCommentForm
from .models import Product, ProductComment


@login_required()
def product_home(request, tag_slug=None):
    query = request.GET.get("product")
    tag = None
    print("query", query)
    if request.GET.get('filter') == 'popular':
        product_ids = [ ac.object_id for ac in Tracker.objects.all() if ac.content_object.__class__.__name__ == 'Product' ]
        product_dict = {}
        for _id in product_ids:
            if _id in product_dict:
                product_dict[uuid.UUID(_id)] = product_dict[_id] +1
            else:
                product_dict[uuid.UUID(_id)] = 1
        sorted_product_dict = dict(sorted(product_dict.items(), key=lambda x:x[1], reverse=True))
    
        popular_product = Product.objects.filter(id__in=sorted_product_dict.keys(), status='public', index=True)
        context = {
            'popular_product':popular_product,
        }
    elif query or tag_slug:
        tag = None

        products = Product.objects.all()
  
        tag = get_object_or_404(Tag, slug=tag_slug)
        item = TaggedItem.objects.filter(tag=tag)

        item = [i.object_id for i in item if i and i !='']
   
 
        # posts = Post.objects.filter(tags__in=["ddd"])
        products = products.filter(id__in=item)
        if query:

            products =products.filter(Q(product_name__icontains=query) | Q(tags__name__icontains=query) | Q(description__icontains=query)).distinct()
        products = products.filter(status='public', index=True).order_by('-updated_date')

    

        context = {
            'query':products,
            'search':query,
            'tag':tag,
        }


    elif request.GET.get('filter') == 'all':
        products = Product.objects.filter(status='public', index=True).order_by('-updated_date')

        context = {
            'products':products
        }
    elif request.GET.get('filter') == 'new':
        new = Product.objects.filter(status='public', index=True).order_by('-created_date')

        context = {
            'new':new
        }
    elif request.GET.get('filter') == 'featured':
        featured = Product.objects.filter(featured=True, status='public', index=True).order_by('-updated_date')

        context = {
            'featured':featured
        }
    elif request.GET.get('filter') == 'seen':
        seen_product_id = [ ac.object_id for ac in Tracker.objects.filter(user=request.user) if ac.content_object.__class__.__name__ == 'Product' ]
        product_dict = {}
        for _id in seen_product_id:
            if _id in product_dict:
                product_dict[_id] = product_dict[_id] +1
            else:
                product_dict[_id] = 1
        sorted_product_dict = dict(sorted(product_dict.items(), key=lambda x:x[1], reverse=True))

        seen_product = Product.objects.filter(id__in=sorted_product_dict.keys(), status='public', index=True)[:6]

        context = {
            'seen_product':seen_product,
        }


    else:
        products = Product.objects.filter(status='public', index=True).order_by('-updated_date')[:6]
        new = Product.objects.filter(status='public', index=True).order_by('-created_date')[:6]
        featured = Product.objects.filter(featured=True, status='public', index=True).order_by('-updated_date')[:6]

      

        product_ids = [ ac.object_id for ac in Tracker.objects.all() if ac.content_object.__class__.__name__ == 'Product' ]
        product_dict = {}
        for _id in product_ids:
            if _id in product_dict:
                product_dict[uuid.UUID(_id)] = product_dict[_id] +1
            else:
                product_dict[uuid.UUID(_id)] = 1
        sorted_product_dict = dict(sorted(product_dict.items(), key=lambda x:x[1], reverse=True))
    
        popular_product = Product.objects.filter(id__in=sorted_product_dict.keys(), status='public', index=True)[:6]

        seen_product_id = [ ac.object_id for ac in Tracker.objects.filter(user=request.user) if ac.content_object.__class__.__name__ == 'Product' ]
        product_dict = {}
        for _id in seen_product_id:
            if _id in product_dict:
                product_dict[_id] = product_dict[_id] +1
            else:
                product_dict[_id] = 1
        sorted_product_dict = dict(sorted(product_dict.items(), key=lambda x:x[1], reverse=True))

        seen_product = Product.objects.filter(id__in=sorted_product_dict.keys(), status='public', index=True)[:6]
    

        context = {
            'products':products,
            'new':new,
            'featured':featured,
            'popular_product':popular_product,
            'seen_product':seen_product
        }
    return render(request, 'scheme/product/product_home.html', context)

@login_required()
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title').lower()
        description = request.POST.get('description')
        project = request.POST.get('project')
        Project_instance = Project.objects.get(pk=project)
        print("Project_instance", Project_instance)
        product_title = Product.objects.filter(product_name=title, author=request.user)
        product_title_len = []
        for i in product_title:
            product_title_len.append(i)
        print("product_title_len======", len(product_title_len))

        if title and len(product_title_len) == 0:
            product = Product.objects.create(product_name=title, author=request.user, project=Project_instance, description=description)
            product.save()
            endpoint = endPoint.objects.create(product=product)
            endpoint.save()
            

            return HttpResponse('Product added')
        return HttpResponse('product title must be unique')
    
    return HttpResponse('Something went wrong')


@login_required()
def edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductEditForm(instance =product)
    
    if request.method == 'POST':
    
        form = ProductEditForm(request.POST or None,request.FILES, instance = product)
        if form.is_valid():
            
            product = form.save(commit=False)
            product.save()
            print("You successfully updated the product")
            return redirect('dashboard:product:product_detail', pk)
        else:
            print(form.errors)
            print('form not valid')

    context = {
        'form':form,
        'product':product
    }


    return render(request, 'scheme/product/edit.html', context)

@login_required()
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    model_len = Model.objects.filter(product=product)
    
    
    endpoint = endPoint.objects.filter(product=product)
    if len(endpoint) == 0:
        endpoint_instance = endPoint.objects.create(product=product)
        endpoint_instance.save()
    
    if len(model_len) == 0:
        model_len_status = True
    else:
        model_len_status = False
    context = {
        'product':product,
        
        'model_form': ModelUploadForm,
     
        'model_len_status': model_len_status
        }
    return render(request, 'scheme/product/product_detail.html', context)


@login_required()
def global_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Tracker.objects.create_from_request(request, product)
    team = get_object_or_404(Project, pk=product.project.pk).team
    comment_form = ProductCommentForm()
    comments = product.comments.filter(active=True).order_by('-created')
    
    developer = get_object_or_404(Team, pk=team.pk).created_by
    print(developer)
    context = {
        'product':product,
        'developer':developer,
        'comment_form':comment_form,
        'comments':comments,

        }
    return render(request, 'scheme/product/global_product_detail.html', context)



@login_required()
def product_play_ground(request, pk):
    product = get_object_or_404(Product, pk=pk)
    script = get_object_or_404(Scripts, product=product)
    Tracker.objects.create_from_request(request, product)

    fields = Fields.objects.filter(scripts=script)

    toDate = datetime.now()
    fromDate = datetime.now() - timedelta(days=30)

    api_log_count = apiplayLog.objects.filter(product=product, user=request.user ,created_date__gte=fromDate, created_date__lte=toDate)

    if len(api_log_count) <= settings.API_PLAY_FREE_COUNT:
        submit = True 
    else:
        submit = False
    if request.method == 'POST':
        print(request.POST)
        field_data = {}
        for i in fields:
            field_data[i.field_name] = request.POST.get(i.field_name)

        print(field_data)

   
        url = f"http://{request.get_host()}/endpoint/play-ground/"
        print(url)

        # Data to send in the GET request
        data = {
          
            "product": product,
            'user':request.user

        }
        data.update(field_data)

        # Send the GET request
        response = requests.get(url, params=data)

        print("response", response.json())

        # Print the response status code
        request.session['play_ground'] = response.json()
    
    if 'play_ground' in request.session:
        content = request.session.get('play_ground')
    else:
        content = None

    context = {
        'product':product,
        'fields':fields,
        'content':content,
        'submit':submit

        }
    return render(request, 'scheme/product/global_product_ground.html', context)


@login_required()
def create_comments(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductCommentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            product_comment = form.save(commit=False)
            product_comment.name = request.user.username
            product_comment.email = request.user.email
            product_comment.product = product

            product_comment.save()
          
        
    comments = product.comments.filter(active=True).order_by('-created')

    print(comments)
    
    context = {
        'comments':comments,
        'product':product,
    }
    return render(request, 'scheme/product/comments/comment_list.html', context)


@login_required()
def comment_list(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = product.comments.filter(active=True).order_by('-created')
    print("comments", comments)
    context = {
        'comments':comments,
        'product':product
    }
    return render(request, 'scheme/product/comments/comment_list.html', context)

# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = ProductCommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)

            reply.name = request.user.username
            reply.email = request.user.email
            
    
            reply.product = Product(pk=post_id)
            reply.parent = ProductComment(pk=parent_id)
           
            reply.save()

           
    print("post_id", post_id)
    product = get_object_or_404(Product, pk=post_id)      
    comments = product.comments.filter(active=True).order_by('-created')
    context = {
        'comments':comments,
        'product':product,
    }
    return render(request, 'scheme/product/comments/comment_list.html', context)


@login_required()
def delete(request, pk):
    context ={}
    cursor = connections['default'].cursor()
    if request.method =="POST":
        print("dict", dict(request.POST), request.POST.getlist('id'))
        for i in request.POST.getlist('id'):
          
            print("i=============", i)

            cursor.execute("PRAGMA foreign_keys = OFF")
            
            cursor.execute(f"""delete from product_product where id='{str(i).replace("-", "")}'""")

            cursor.execute("PRAGMA foreign_keys = ON")
            # Product.objects.filter(id=i).delete()
            # print("obj============", obj)
            # delete object
            # obj.delete()
        return redirect('dashboard:projects:project_detail', pk)
 
    return HttpResponse("Something went wrong")


