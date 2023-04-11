from django.urls import path
from .views import *


app_name = 'api'


urlpatterns=[
    path('', api_home, name='api_home'),
    path('add/', add, name='add'),
    path('delete/', delete, name='delete'),
    path('<uuid:pk>/', api_detail, name='api_detail'),

]