from django.urls import path
from .views import *


app_name = 'product'


urlpatterns=[

    path('',product_home,name='product_home'),
    path('add/', add, name='product_add'),
    path('p/<uuid:pk>/', product_detail, name='product_detail'),
    path('edit/<uuid:pk>', edit, name='product_edit'),
    path('delete/<uuid:pk>/', delete, name='delete'),
    
    path('<uuid:pk>/', global_product_detail, name='global_product_detail'),
    path('<uuid:pk>/try/', product_play_ground, name='product_play_ground'),
    path('tag/<slug:tag_slug>/',product_home, name='product_tag'),

    path('create_comments/<uuid:pk>/', create_comments, name='create_comments'),
    path('comment_list/<uuid:pk>/', comment_list, name='comment_list'),
    path('reply_page/', reply_page, name='reply_page'),
    
    
]