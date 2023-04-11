import re

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings


from .models import Newsletter, Contact
from .text import enquiry_message

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard_home')
    else:
        context = {}
        return render(request, 'common/home.html', context)

def aboutus(request):
    context = {}
    return render(request, 'common/aboutus.html', context)

def contactus(request):
    context = {}
    return render(request, 'common/contactus.html', context)

def tmac(request):
    context = {}
    return render(request, 'common/tmac.html', context)

def privacy(request):
    context = {}
    return render(request, 'common/privacy-policy.html', context)

def faq(request):
    context = {}
    return render(request, 'common/faq.html', context)

def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div style='color:red;'> This username already exists</div>")
    else:
        return HttpResponse("<div style='color:green;'>This username available</div>")

def check_email(request):
    email_text = request.POST.get('email')
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(pat,email_text):
        if get_user_model().objects.filter(email=email_text).exists():
            return HttpResponse("<div style='color:red;'> This email already exists</div>")
        else:
            return HttpResponse("<div style='color:green;'>This email available</div>")
    else:
        return HttpResponse("<div style='color:red;'> Not an Email format</div>")


def save_newsletter(request):
    if request.method == "POST":
        email_text = request.POST.get('newsletter_email')
        print('email_text', email_text)
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(pat,email_text):
            Newsletter.objects.create(
                email=email_text
            )

            return HttpResponse("Success")
      
    return HttpResponse("Failed")


def save_contact(request):
    if request.method == "POST":
        email_text = request.POST.get('email')
        fullname_text = request.POST.get('fullname')
        phone_text = request.POST.get('phone')
        detail_text = request.POST.get('detail')
   
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(pat,email_text):
            Contact.objects.create(
                full_name = fullname_text,
                email=email_text,
                phone = phone_text,
                detail = detail_text
            )

            subject = f"enquiry received {settings.SITE_NAME} (emergency)"
            message = enquiry_message.format(fullname=fullname_text,email=email_text, phone=phone_text,detail=detail_text, SITE_OWNER=settings.SITE_OWNER)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = settings.CONTACT_EMAIL_LIST
            send_mail(subject, message, email_from, recipient_list)

            return HttpResponse("Success")
      
    return HttpResponse("Failed")

