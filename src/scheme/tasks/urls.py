from django.urls import path
from .views import *


app_name = 'tasks'


urlpatterns=[
    
    path('add/',add,name='task_add'),
    
]