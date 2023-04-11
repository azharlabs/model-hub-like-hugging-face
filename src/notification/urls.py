from django.urls import path, re_path, reverse_lazy
from .views import *


app_name = 'notification'


urlpatterns=[
    path('save_permission/', save_permission, name='save_permission')

]