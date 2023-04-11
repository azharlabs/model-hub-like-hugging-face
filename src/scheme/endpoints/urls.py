from django.urls import path
from .views import *


app_name = 'endpoint'


urlpatterns=[
    path('', endpoint, name='endpoint'), 
    path('play-ground/', endpoint_play, name='endpoint_play'),
]