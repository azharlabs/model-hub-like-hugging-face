from django.urls import path, include
from .views import *


app_name = 'dashboard'


urlpatterns=[

    path('', home, name='dashboard_home'),

    path("teams/", include('scheme.teams.urls', namespace='teams')),
    path("fields/", include('scheme.fields.urls', namespace='fields')),
    path("files/", include('scheme.files.urls', namespace='files')),
    path("model/", include('scheme.model.urls', namespace='model')),
    path("tasks/", include('scheme.tasks.urls', namespace='tasks')),
    path("product/", include('scheme.product.urls', namespace='product')),
    path("projects/", include('scheme.projects.urls', namespace='projects')),
    path("scripts/", include('scheme.scripts.urls', namespace='scripts')),
]