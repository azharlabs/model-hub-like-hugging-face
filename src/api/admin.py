from django.contrib import admin
from .models import API, apiLog, apiplayLog

admin.site.register(API)

admin.site.register(apiLog)

admin.site.register(apiplayLog)