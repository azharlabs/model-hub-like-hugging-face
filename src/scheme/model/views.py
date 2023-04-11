import joblib

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from .forms import ModelUploadForm
from scheme.product.models import Product
from common.utils import validate_pickle_file
from .models import Model


@login_required()
def model_home(request):
    context = {}
    return render(request, 'scheme/model/model_home.html', context)


@login_required()
def add(request, pk):
    form = ModelUploadForm()
    if request.method == 'POST':
        print('request.post==================', request.FILES)
        form = ModelUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_name')
        product = get_object_or_404(Product, pk=pk)
        product_len = Model.objects.filter(product=product)
        print("product_len========", len(product_len))
        if len(product_len) == 0:
            if form.is_valid():

                for f in files:
                    print("f==============", f)
                    if validate_pickle_file(f) == True:

                        try:
                           
                            print("loaded", joblib.load(f))
                            model_code = joblib.load(f)
                            file_instance = Model.objects.create(file_name=f, author=request.user, product=product,model_name=str(f))
                    
                    
                            file_instance.save()
                        except:
                            messages.error(request, 'model not properly wrappered')
                    else:
                        messages.error(request, 'Only support *.pkl format' )


                return redirect('dashboard:product:product_detail', pk)
            else:
                messages.error(request, form.errors )
        else:
            messages.error(request, 'Model already uploaded you can able to upload one model per product' )
        return redirect('dashboard:product:product_detail', pk)
    
    return redirect('dashboard:product:product_detail', pk)


@login_required()
def model_detail(request, pk):

    product = get_object_or_404(Product, pk=pk)

    model_code_path = get_object_or_404(Model, product=product).file_name

    model = get_object_or_404(Model, product=product)
    model_code = 'model not Properly wrappered '
    try:
        model_code = joblib.load(str(settings.MEDIA_ROOT)+ '/' + str(model_code_path))
    except:
        messages.error(request, 'model not properly wrappered')

    
    context = {
        'contents':model_code,
        'model':model
    }

    return render(request, 'scheme/model/detail.html', context)