import json
from datetime import datetime, timedelta
from subprocess import Popen, PIPE


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response 

from scheme.product.models import Product
from api.models import API, apiLog, apiplayLog
from scheme.fields.models import Fields
from scheme.scripts.models import Scripts
from .models import endPoint
from accounts.models import Billing
 



def endpoint(request):
    if request.method == 'POST':
        data = dict(request.POST)
        print(data)
    else:
        data = dict(request.GET)


    print("data",data)
    
    if 'api' in data:
        api = API.objects.filter(api=data['api'][0]) #get_object_or_404(API, api=data['api'])
        print("api", data['api'])
        if api:
            api = api[0]
            request_user = api.user
            
            if request_user.billing.stripe_payment_method_id:

                if 'product' in data:
                    product = Product.objects.filter(product_name=data['product'][0].lower()) #get_object_or_404(Product, product_name=data['product'])
                    print("product", product)
                    if product:
                        product = product[0]
                        script = get_object_or_404(Scripts, product=product)
                        field_query = Fields.objects.filter(scripts=script)
                        fields = [i.field_name for i in field_query]
                        for i in fields:
                            if i not in data:
                                return JsonResponse({'error': f"field '{i}' not present in the url"})

                        if product.price_per_request:
                            price = product.price_per_request + (product.price_per_request *0.2)
                        else:
                            price = 0.02

                        toDate = datetime.now()
                        fromDate = datetime.now() - timedelta(days=30)
                        
                        api_log_count = apiLog.objects.filter(api=api, product=product, created_date__gte=fromDate, created_date__lte=toDate)
                        print("price", price)
                        if len(api_log_count) >= settings.API_FREE_COUNT:
                            apilog = apiLog.objects.create(api=api, product=product, price=price)
                            apilog.save()

                        endpoint = get_object_or_404(endPoint, product=product).endpoint_file
                        print(endpoint)

                        args = [str(data[i][0]) for i in fields]

                        endpoint_file_path = str(settings.MEDIA_ROOT)+'/' + str(endpoint)
                        print("endpoint_file_path", endpoint_file_path)

                        output = Popen([f"{settings.VIRTUAL_PYTHON_PATH}", endpoint_file_path] + args, stdout=PIPE, stderr=PIPE)

                        out, err = output.communicate()
                        print(type(json.loads(json.dumps(out.decode()))), json.loads(json.dumps(out.decode())))

                        try:
                            out_json = json.loads(out.decode().replace("'", '"'))
                            print(out_json)
                            print(type(out_json))
                            return JsonResponse(out_json, safe=False)
                        except ValueError:
                            return JsonResponse({'error': 'Output is not an proper json format'})

                    else:
                        return JsonResponse({'error': 'Wrong product name'})

                else:

                    return JsonResponse({'error': 'product not present in the url'})
            else:
                return JsonResponse({'error': 'Connect with your billing account'})
        else:
            return JsonResponse({'error': 'Wrong api key'})
    
    else:
    
        return JsonResponse({'error': 'api is not present in the url'})
   
   
    return JsonResponse({'error': 'something went wrong'})



def endpoint_play(request):
    if request.method == 'POST':
        data = dict(request.POST)
        print("post data", data)
    else:
        data = dict(request.GET)


    print("data",data)


    

    if 'product' in data:
        product = Product.objects.filter(product_name=data['product'][0].lower()) #get_object_or_404(Product, product_name=data['product'])
        print("product", product)
        if product:
            print("data.get('user')", data.get('user'))
            user = get_object_or_404(User, username=data.get('user')[0])
            product = product[0]
            script = get_object_or_404(Scripts, product=product)
            field_query = Fields.objects.filter(scripts=script)
            fields = [i.field_name for i in field_query]
            for i in fields:
                if i not in data:
                    return JsonResponse({'error': f"field '{i}' not present in the url"})

            if product.price_per_request:
                price = product.price_per_request + (0.2*(product.price_per_request))
            else:
                price = 0.02


            apilog = apiplayLog.objects.create(user=user, product=product, price=price)
            apilog.save()



            endpoint = get_object_or_404(endPoint, product=product).endpoint_file
            print(endpoint)

            args = [str(data[i][0]) for i in fields]

            print("args=================", args)

            endpoint_file_path = str(settings.MEDIA_ROOT)+'/' + str(endpoint)
            print("endpoint_file_path", endpoint_file_path)

            output = Popen([f"{settings.VIRTUAL_PYTHON_PATH}", endpoint_file_path] + args, stdout=PIPE, stderr=PIPE)

            out, err = output.communicate()
            print(type(json.loads(json.dumps(out.decode()))), json.loads(json.dumps(out.decode())))

            

            
            try:

                
                out_json = json.loads(out.decode().replace("'", '"'))
                print(out_json)
                print(type(out_json))
                return JsonResponse(out_json, safe=False)
            except ValueError:
                return JsonResponse({'error': 'Output is not an proper json format'})

        else:
            return JsonResponse({'error': 'Wrong product name'})

    else:

        return JsonResponse({'error': 'product not present in the url'})
