from django.urls import path
from .views import *

app_name  = "membership"

urlpatterns = [
    path('auth/settings', member_settings, name='settings'),
    path('join', join, name='join'),
    path('checkout', checkout, name='checkout'),
    path('success',success, name='success'),
    path('cancel', cancel, name='cancel'),
    path('updateaccounts', updateaccounts, name='updateaccounts'),
]