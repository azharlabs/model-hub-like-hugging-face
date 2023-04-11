from datetime import datetime, timedelta

from tracking_analyzer.models import Tracker

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import Profile
from blog.models import Post
from api.models import API, apiLog
from scheme.product.models import Product
from scheme.projects.models import Project
from scheme.teams.models import Team



@login_required
def home(request):
    teams = Team.objects.filter(created_by=request.user)
    projects = Project.objects.filter(team__in=teams)
    products = Product.objects.filter(project__in=projects)

    api_log = apiLog.objects.filter(product__in=products)

    not_indexed = products.filter(index=False)

    toDate = datetime.now()
    fromDate = datetime.now() - timedelta(days=30)

    api_earnings = api_log.filter(created_date__gte=fromDate, created_date__lte=toDate).order_by('created_date')

  

    last_30_days = {}
    start = 0
    for i in range(30):
        i +=1
        for earning in api_earnings:
            # print((fromDate + timedelta(days=start)).strftime("%d-%m-%Y"), earning.created_date.strftime("%d-%m-%Y"))
            if (fromDate + timedelta(days=start)).strftime("%d-%m-%Y") == earning.created_date.strftime("%d-%m-%Y"):
                # print(i, "True", float(earning.price))
                if str(i) in last_30_days:
                    last_30_days[str(i)] = last_30_days[str(i)] + float(earning.price)
                else:
                    last_30_days[str(i)] = float(earning.price)
                # print(last_30_days)
        
            else:
                if str(i) not in last_30_days:
                    last_30_days[str(i)] = 0
        start += 1



    
    earning = 0
    products = []
    for api in api_log:
        earning += api.price
        products.append(api.product)


    product_clicked = [str(ac.object_id) for ac in Tracker.objects.all() if ac.content_object.__class__.__name__ == 'Product']
    print("products", products)
    if products:
        for product in products:
        
            if str(product.id) not in product_clicked:
                product_clicked.remove(str(product.id))
        # print("product_clicked", product_clicked)
    else:
        product_clicked = []

    top_products_dict = {}
    for i in product_clicked:
        if i in top_products_dict:
            top_products_dict[i] +=1
        else:
            top_products_dict[i] = 1

    top_products_dict = dict(sorted(top_products_dict.items(), key=lambda item: item[1]))

    top_products = Product.objects.filter(id__in=list(top_products_dict.keys())[:5])

    top_product_object = {}
    for i in top_products:
        top_product_object[i.id] = i.product_name


    # print('top_products', top_products)

    blogs = Post.objects.filter(author=request.user)


    blog_clicked = [str(ac.object_id) for ac in Tracker.objects.all() if ac.content_object.__class__.__name__ == 'Post']
    # print('blog_clicked', blog_clicked)

    if blogs:
        for blog in blogs:
        
            if str(blog.id) not in blog_clicked:
                blog_clicked.remove(str(blog.id))
        # print("product_clicked", product_clicked)
    else:
        blog_clicked = []

    top_blogs_dict = {}
    for i in blog_clicked:
        if i in top_blogs_dict:
            top_blogs_dict[i] +=1
        else:
            top_blogs_dict[i] = 1

    top_blogs_dict = dict(sorted(top_blogs_dict.items(), key=lambda item: item[1]))

    top_blogs = Post.objects.filter(id__in=list(top_blogs_dict.keys())[:5])

    top_blog_object = {}
    for i in top_blogs:
        top_blog_object[i.id] = i.title[:12]+str('...')


    

    
    users_all = []
    for team in teams:

        users_all.append(team.members.all())
    users = {}
    for user in users_all:
        for i in user:
            # print("user", user)
            if i.username not in users:
                users[i.username] = i

    # profile = Product.objects.filter(user__in=list(users.values()))



    # print("last_30_days", last_30_days)

    
    context = {
        'employess':list(users.values()),
        'total_request':len(api_log),
        'total_products':len(products),
        'product_clicked':len(product_clicked),
        'earning':earning,
        'not_indexed':not_indexed,
        'lost30':list(last_30_days.keys()),
        'lost30_value':["{:.2f}".format(float(i)) for i in last_30_days.values()],
        'top_5_product':list(top_product_object.values()),
        'top_5_product_value': list(top_products_dict.values()),
        'top_5_blog':list(top_blog_object.values()),
        'top_5_blog_value': list(top_blogs_dict.values()),
        'teams':teams

    }
    return render(request, 'scheme/dashboard/dashboard_home.html', context)