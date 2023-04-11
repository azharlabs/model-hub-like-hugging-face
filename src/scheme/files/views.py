import pandas as pd
import pandas_profiling
from bs4 import BeautifulSoup

from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import Files, UpdateFileInfo
from .forms import ScriptFileUploadForm
from common.utils import validate_file
from scheme.projects.models import Project

@login_required()
def files_home(request):
    context = {}
    return render(request, 'scheme/files/files_home.html', context)


@login_required()
def add(request, pk):
    form = ScriptFileUploadForm()
    if request.method == 'POST':
        print('request.post==================', request.POST)
        form = ScriptFileUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('script_file')
        project = get_object_or_404(Project, pk=pk)
        print("files========", files)
        if form.is_valid():

            for f in files:
                print("f==============", f)
                if validate_file(f) == True:

                    df = pd.read_csv(f)
                    df.to_parquet(f'{f}.parquet', engine='pyarrow', index=False)

                    
                    
                 
                    file_instance = Files(author=request.user, project=project, script_name=str(f))
                    with open(f'{f}.parquet', 'rb') as parquet:
                        file_instance.script_file.save(f'{f}.parquet', File(parquet))
                        file_instance.save()
                 
                    
                    
                else:
                    messages.error(request, 'Only support *.csv format' )


            return redirect('dashboard:projects:projects_files', pk)
        return redirect('dashboard:projects:projects_files', pk)
    
    return redirect('dashboard:projects:projects_files', pk)

@login_required()
def file_detail(request, pk):
    script_file = get_object_or_404(Files, pk=pk).script_file

    df = pd.read_parquet(script_file, engine='pyarrow')
    df = df.head(11)
    files = get_object_or_404(Files, pk=pk)
    
    context = {
        'contents':df.to_html(classes='table table-bordered', index=False),
        'files':files
    }
    return render(request, 'scheme/files/files_details.html', context)


@login_required()
def analytics(request, pk):

    files = get_object_or_404(Files, pk=pk)
    # Extract all the HTML elements inside the div element
    
    context = {
        'files':files,
   
    }

    return render(request, 'scheme/files/analytics.html', context)

@xframe_options_exempt
def edit(request, pk):

    files = get_object_or_404(Files, pk=pk)
    df = pd.read_parquet(files.script_file, engine='pyarrow')
    print(df)
    data = pandas_profiling.ProfileReport(df, minimal=True)
    print(data)
    # Parse the HTML document
    soup = BeautifulSoup(data.to_html(), 'html.parser')



    div = soup.find('footer')
    soup = str(soup).replace(str(div.extract()),'')
    div = BeautifulSoup(soup).find('nav')
    soup = str(soup).replace(str(div.extract()),'')

 




    # Extract all the HTML elements inside the div element
    

    context = {
        'files':files,
        'data':soup,
    }


    return render(request, 'scheme/files/edit.html', context)

