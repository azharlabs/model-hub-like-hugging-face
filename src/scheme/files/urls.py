from django.urls import path
from .views import *


app_name = 'files'


urlpatterns=[

    path('',files_home,name='files_home'),
    path('add/<uuid:pk>/', add, name='files_add'), 
    path('<uuid:pk>/', file_detail, name='file_detail'),
    path('edit/<uuid:pk>', edit, name='file_edit'),
    path('analytics/<uuid:pk>/', analytics, name='analytics'),
]