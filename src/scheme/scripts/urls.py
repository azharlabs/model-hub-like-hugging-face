from django.urls import path
from .views import *


app_name = 'scripts'


urlpatterns=[

    path('',scripts_home,name='scripts_home'),
    path('add/<uuid:pk>/', add, name='script_add'),
    path('<uuid:pk>/', script_detail, name='script_detail'),
    path('edit/<uuid:pk>/', edit, name='script_edit'),

    path('create_comments/<uuid:pk>/', create_comments, name='create_comments'),
    path('comment_list/<uuid:pk>/', comment_list, name='comment_list'),
    path('reply_page/', reply_page, name='reply_page'),

]