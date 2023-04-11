from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import EmailNotification

@login_required
def save_permission(request):
    if request.method == "POST":
        print("notification request method", dict(request.POST))

        notification_permission = dict(request.POST)

        if 'feature_update' in notification_permission.keys():
            feature_update = True
        else:
            feature_update = False

        if 'interested_blog_update' in notification_permission.keys():
            interested_blog_update = True
        else:
            interested_blog_update = False

        if 'new_device_signin' in notification_permission.keys():
            new_device_signin = True
        else:
            new_device_signin = False
          
 
        EmailNotification.objects.filter(user=request.user).update(
            feature_update = feature_update,
            interested_blog_update = interested_blog_update,
            new_device_signin = new_device_signin
        )

        return HttpResponse("Notification Permission Saved")
      
    return HttpResponse("Something went wrong")