from django.urls import path
from .views import *


app_name = 'projects'


urlpatterns=[
    
    path('',projects_home,name='projects_home'),
    path('d/<uuid:pk>/', project_detail, name='project_detail'),
    path('add/', add, name='projects_add'),
    path('edit/<uuid:pk>/', edit, name='projects_edit'),
    path('delete/', delete, name='delete'),

    path('d/<uuid:pk>/files/', projects_files, name='projects_files'),
]