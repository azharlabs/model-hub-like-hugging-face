from django.urls import path
from .views import *


app_name = 'teams'


urlpatterns=[

    path('',team_home,name='team_home'),
    path('add/', add, name='team_add'),
    path('d/<uuid:pk>/', team_detail, name='team_detail'),
    path('delete/', delete, name='delete'),
    

    path('invite/', invite, name='invite'),
    path('accept_invitation/', accept_invitation, name='accept_invitation'),

]