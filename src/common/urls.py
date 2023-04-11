from django.urls import path
from .views import *

app_name = 'common'



urlpatterns=[
    path('',home,name="home"),
    path('aboutus/',aboutus,name="aboutus"),
    path('contactus/',contactus,name="contactus"),
    path('tmac/',tmac,name="tmac"),
    path('privacy/',privacy,name="privacy"),
    path('faq/',faq,name="faq"),

    path('check_username/', check_username, name='check_username'),
    path('check_email/', check_email, name='check_email'),

    path('save_newsletter/', save_newsletter, name='save_newsletter'),
    path('save_contact/', save_contact, name='save_contact')

]