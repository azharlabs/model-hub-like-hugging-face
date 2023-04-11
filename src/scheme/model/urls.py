from django.urls import path
from .views import *


app_name = 'model'


urlpatterns=[

    path('',model_home,name='model_home'),
    path('add/<uuid:pk>/', add, name='model_add'),
    path('<uuid:pk>/', model_detail, name='model_detail')
]