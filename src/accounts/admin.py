from django.contrib import admin
from .models import Profile, Follow, Billing, Preferences

admin.site.register(Profile)

admin.site.register(Follow)
admin.site.register(Billing)
admin.site.register(Preferences)