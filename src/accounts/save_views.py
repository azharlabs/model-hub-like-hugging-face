import re 

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from common.utils import get_random_password
from common.text import welcome_message, email_message_changed
from .models import Profile, Preferences
from .forms import BasicinfoForm, ProfileInfoForm
from notification.models import EmailNotification



@login_required
def save_basicinfo(request):
    if request.method == "POST":
     
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        account_type1 = request.POST.get('account_type1', '')
        account_type2 = request.POST.get('account_type2', '')
        address1 = request.POST.get('address1', '')
        adddress2 = request.POST.get('adddress2', '')
        zipcode = request.POST.get('zipcode', '')
        if account_type1 and account_type1 != '':
            account_type = 'individual'
        else:
            account_type = 'company'
 
        Profile.objects.filter(user=request.user).update(
            first_name = firstname,
            last_name = lastname,
            phone = phone,
            company = company,
            account_type = account_type,
            address1 = address1,
            address2 = adddress2,
            zip_code = zipcode
            

        )

        return HttpResponse("Success")
      
    return HttpResponse("Failed")



@login_required
def save_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.user.username
        account_url = ''
        old_email = request.user.email
        if email and email != '':
            pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.match(pat,email):
                User.objects.filter(username=request.user.username).update(email=email)
                subject = f"Email Address is changed"
                message = email_message_changed.format(username=username,new_email=email,account_url=account_url, SITE_OWNER=settings.SITE_OWNER)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [old_email, ]
                send_mail(subject, message, email_from, recipient_list)
                return HttpResponse(f"Email is changed")
            return HttpResponse(f"{email} this is not a correct email format")
        return HttpResponse("Empty value is not an email")
    return HttpResponse("Something went wrong contact admin")
     
@login_required
def save_preferences(request):
    if request.method == "POST":
        print("account Preferences request method", dict(request.POST))

        account_Preferences = dict(request.POST)

        if 'early_release' in account_Preferences.keys():
            early_release = True
        else:
            early_release = False

        if 'profile_viewed' in account_Preferences.keys():
            profile_viewed = True
        else:
            profile_viewed = False
          
 
        Preferences.objects.filter(user=request.user).update(
            early_release = early_release,
            profile_viewed = profile_viewed
        )

        return HttpResponse("Account Preferences Saved")
      
    return HttpResponse("Something went wrong")