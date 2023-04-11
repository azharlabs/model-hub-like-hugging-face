from django.urls import path
from .views import *

app_name = 'solutions'



urlpatterns=[

    path('', solutions, name='home'),

    path('data-preprocessing/auto/', auto, name='auto'),
    path('data-preprocessing/data-preparation/', data_preparation, name='data_preparation'),
    path('data-preprocessing/scale-and-transform/', scale_and_transform, name='scale_and_transform'),
    path('data-preprocessing/feature-engineering/', feature_engineering, name='feature_engineering'),
    path('data-preprocessing/feature-selection/', feature_selection, name='feature_selection'),

    path('modules/supervised/', supervised, name='supervised'),
    path('modules/unsupervised/', unsupervised, name='unsupervised'),
    path('modules/time-series/', timeseries, name='timeseries'),

    path('modules/supervised/classification/', classification, name='classification'),
    


]