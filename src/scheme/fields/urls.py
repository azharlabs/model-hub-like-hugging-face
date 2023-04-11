from django.urls import path
from .views import *


app_name = 'fields'


urlpatterns=[

    path('',fields_home,name='fields_home'),
    path('addscriptfield_form/', addscriptfield_form, name='addscriptfield_form'),
    path('create_fields/<uuid:pk>/', create_fields, name='create_fields'),
    path('field_list/<uuid:pk>/', field_list, name='field_list'),
    path('delete/<uuid:pk>/', delete, name='delete'),
]