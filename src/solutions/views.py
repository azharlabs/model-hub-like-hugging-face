from io import StringIO
import pandas as pd
import ast
pd.options.display.max_columns = None
from subprocess import Popen, PIPE
from pathlib import Path    

from django.conf import settings
from django.contrib import messages 
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from scheme.files.models import Files
from .forms import pandasScriptEditForm
from .models import pandasCode


@login_required()
def solutions(request):
    context = {}
    return render(request, 'solutions/home.html', context)

@login_required()
def auto(request):
    pk = request.GET.get('data')
    script_file = get_object_or_404(Files, pk=pk).script_file

    df = pd.read_parquet(script_file, engine='pyarrow')
    df = df.head(11)
    files = get_object_or_404(Files, pk=pk)
    
    context = {
        'contents':df.to_html(classes='table table-bordered', index=False),
        'files':files
    }
    return render(request, 'solutions/datapreprocessing/auto.html', context)

@login_required()
def data_preparation(request):
    context = {}
    return render(request, 'solutions/datapreprocessing/data_preparation.html', context)

@login_required()
def scale_and_transform(request):
    context = {}
    return render(request, 'solutions/datapreprocessing/scale_and_transform.html', context)

@login_required()
def feature_engineering(request):
    context = {}
    return render(request, 'solutions/datapreprocessing/feature_engineering.html', context)

@login_required()
def feature_selection(request):
    context = {}
    return render(request, 'solutions/datapreprocessing/feature_selection.html', context)

@login_required()
def supervised(request):
    context = {}
    return render(request, 'solutions/modules/supervised.html', context)

@login_required()
def unsupervised(request):
    context = {}
    return render(request, 'solutions/modules/unsupervised.html', context)

@login_required()
def timeseries(request):
    context = {}
    return render(request, 'solutions/modules/timeseries.html', context)



@login_required()
def classification(request):

    print("dict============", dict(request.GET))
    data_dict = dict(request.GET)
    # {'csrfmiddlewaretoken': ['KrNOpRJnEPnz1CqUs7qA8bqF78cIw37C4dekQRAXxGnQ2tqCDhOBJf5IStNjZHPY'], 'target': ['Age'], 'execute': ['True'], 'data': ['918b24e4-8787-4bfa-8664-93e7a57ec948']}
    pk = data_dict.get('data')[0]
    
    data = get_object_or_404(Files, pk=pk)

    padas_code_check = pandasCode.objects.filter(data=data, model_type='classification')

    print("length_pandas_code", len(padas_code_check))
    if len(padas_code_check) == 0:
        pandasCode.objects.create(data=data, model_type='classification', author=request.user)

    pandas_code = get_object_or_404(pandasCode, data=data)
    pandas_form = pandasScriptEditForm(request.POST or None,instance=pandas_code)


    if pandas_form.is_valid():
        pandas_form_code = pandas_form.save(commit=False)
        pandas_form_code.save()

        
        print("================pandas_form_code===========", pandas_form_code)
    
    script_file = data.script_file

    if pandas_code.pandas_code:
        with open('pandas_code.py', 'w') as f:
            f.write('import sys\n')
            f.write("sys.path.append('E:/tool/venv\Lib\site-packages')\n")
            f.write('import pandas as pd\n\n\n')
            f.write("pd.set_option('display.max_columns', None)\n\n\n")
            
           
            
            f.write('def dataframe():\n\n')
            f.write(f"    df = pd.read_parquet('E:/tool\src\media/{script_file}', engine='pyarrow')\n")
            f.write(f"    df.columns = df.columns.str.upper()\n")
            print("code=======", pandas_code.pandas_code)
            n = pandas_code.pandas_code.split('\n')
            print("n==========", n)
            for code in n:
                if 'print' not in code:
                    print("code", code)
                    f.write(f"    {code}\n")
            # f.write(f"    print(df)\n\n")
            f.write(f"    df = df.head(5)\n\n")
            f.write(f"    return list(df.columns), list(df.values)\n\n")

             
            f.write('print(dataframe())\n')
        
            
        path = Path('pandas_code.py')
        output = Popen([f"{settings.VIRTUAL_PYTHON_PATH}", path], stdout=PIPE, stderr=PIPE)

        out, err = output.communicate()
        print("out-----------------", type(out))
        print("err-----------------", str(err), type(str(err)))
        if str(err) != "b''" and str(err) != '' and err != None:
            messages.error(request, str(err))
            df = pd.DataFrame()
        else:
           
            data_str = out.decode()
            data_str = data_str.replace('\r\n', '').replace('(', '').replace(')', '').replace('Timestamp', '').replace('array', '').replace('dtype=object', '').replace(' , ', '')
            data_list = ast.literal_eval(data_str)
            df = pd.DataFrame(data_list[1], columns=data_list[0])
    else:
        df = pd.read_parquet(script_file, engine='pyarrow')
        df = df.head(5)
    # df = pd.read_parquet(script_file, engine='pyarrow')
    print("========df=============", df)

    df_sample = df.head(5)
    print(df_sample)

    if 'execute' in data_dict:
        with open('train.py', 'w') as f:
            f.write('import sys\n')
            f.write("sys.path.append('E:/tool/venv\Lib\site-packages')\n")

            f.write('import pandas as pd\n')
            f.write('from pycaret.classification import *\n\n\n')
            f.write('import warnings\n')
            f.write("warnings.filterwarnings('ignore')\n\n\n")
            f.write("pd.set_option('display.max_columns', None)\n\n\n")

            f.write('def execute():\n\n')
            f.write(f"    df = pd.read_parquet('E:/tool\src\media/{script_file}', engine='pyarrow')\n")
            f.write(f"    df.columns = df.columns.str.upper()\n")
            n = pandas_code.pandas_code.split('\n')
            for code in n:
                if 'print' not in code:
                    print("code", code)
                    f.write(f"    {code}\n")
            f.write(f"    s = setup(data = df, target ='{data_dict.get('target')[0]}', silent=True)\n")
            f.write(f"    best = compare_models()\n")
            f.write(f"    save_model(best, 'best_model')\n")

            f.write(f"execute()\n")



        path = Path('train.py')
        train = Popen([f"{settings.VIRTUAL_PYTHON_PATH}", path], stdout=PIPE, stderr=PIPE)

        out, err = train.communicate()
        print("out-----------------", out)
        print("err-----------------", str(err), type(str(err)))
        if str(err) != "b''" and str(err) != '' and err != None:
            messages.error(request, str(err))
            df = pd.DataFrame()
        else:
            messages.success(request, "traing completed")

        # s = setup(data = df, target =data_dict.get('target')[0], silent=True)

    print("columns", list(df.columns), df_sample.values)
    files = get_object_or_404(Files, pk=pk)
    
    context = {
        # 'contents':df_sample.to_html(classes='table table-bordered', index=False),
        'files':files,
        'columns': list(df_sample.columns),
        'data_values':df_sample.values,
        'pandas_form':pandas_form,
        'pandas_code':pandas_code.pandas_code
    }
    return render(request, 'solutions/modules/supervised/classification.html', context)
