import re 
import stripe 

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from scheme.teams.models import Invitation, Team
from common.utils import get_random_password
from common.text import welcome_message, email_message_changed
from .models import Profile, Preferences
from .forms import BasicinfoForm, ProfileInfoForm, PayoutForm
from notification.models import EmailNotification
from .signals import user_logged_in
from tracking_analyzer.models import Tracker
from analytics.signals import object_viewed_signal



def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = get_random_password(12)

        user = User.objects.create_user(
            username = username,
            password = password,
            email = email
        )

        subject = f"Welcome to {settings.SITE_NAME} (confidential)"
        message = welcome_message.format(username=username,SITE_NAME=settings.SITE_NAME, password=password, SITE_OWNER=settings.SITE_OWNER)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('accounts:login')

    context = {}
    return render (request, "accounts/signup.html", context)



def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(pat,username):
            print("email true")
            username = User.objects.get(email=username.lower()).username
            user = authenticate(username=username, password=password)
        else:
            user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
          

            invitations = Invitation.objects.filter(email=user.email, status=Invitation.INVITED)

            if invitations:
                return redirect('dashboard:teams:accept_invitation')
            else:
               
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard:dashboard_home")
        else:
            messages.error(request,"Invalid username or password.")
    context = {}
    return render(request, 'accounts/login.html', context)

@login_required
def logout_page(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("common:home")


@login_required
def account_settings(request):
    cancel_at_period_end = False
    membership = False
    user = request.user
    
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile_form = ProfileInfoForm(request.POST,  request.FILES,instance=profile)
        if profile_form.is_valid():
           profile_form.save(commit=False)
           profile_form.user = user
           profile_form.save()
           print('Uploaded Successfully')
        else:
            print(profile_form.errors)
    else:
        profile_form = ProfileInfoForm()
    preference_data = Preferences.objects.get(user=user)
    profile_data = Profile.objects.get(user=user)
    notification_data = EmailNotification.objects.get(user=user)
    user_data = User.objects.get(username=user.username)

    try:
        if request.user.customer.membership:
            membership = True
        if request.user.customer.cancel_at_period_end:
            cancel_at_period_end = True
    except Customer.DoesNotExist:
        membership = False

    print("profile_data", profile_data)
    print("notification_data", notification_data)
    print("user_data", user_data)
    context = {
        'profile_data': profile_data,
        'membership':membership,
        'cancel_at_period_end':cancel_at_period_end,
        'notification_data': notification_data,
        'user_data':user_data,
        'profile_form':profile_form,
        'preference_data':preference_data,
        'payout_form':PayoutForm(instance=profile)
    }
    return render(request, 'accounts/account_settings.html', context)

@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        print(old_password, new_password1, new_password2)
        if old_password and new_password1 and new_password2:
            if len(new_password1) >= 8:
                if new_password1 == new_password2:
                    if new_password1 != old_password:
                        user = authenticate(username=request.user.username,password=old_password)
                        print("user", user)
                        try:
                            if user is not None:
                                u = User.objects.get(username=request.user.username)
                                u.set_password(new_password1)
                                u.save()
                                return HttpResponse("Password changes Successfully")
                            else:
                                return HttpResponse("user is not exist or wrong password")
                        except:
                            return HttpResponse("Something went wrong contact admin")
                    return HttpResponse("New password should not same as old password")
                return HttpResponse("Password not matching")
            return HttpResponse("Password length should greater then or equal to 8")
        return HttpResponse("Please fill all the fields")
    return HttpResponse("Something went wrong contact admin")


@login_required()
def my_profile(request, pk):
    # user = Profile.user
    profile=get_object_or_404(Profile, pk=pk)
    Tracker.objects.create_from_request(request, profile.user)
    object_viewed_signal.send(profile.user.__class__, instance=profile.user, request=request)
    followers = profile.followers.all()
    print("followers=====", followers)
    if len(followers) == 0:
        is_following = False
    for follower in followers:
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False
    number_of_followers = len(followers)
    # following_count = Profile.objects.filter(followers=pk).count()

    context = {
        'profile':profile,
        'number_of_followers': number_of_followers,
        'is_following': is_following,
        # 'following_count':following_count,
    }
    return render(request, 'accounts/my-profile.html', context)

@login_required()
def followers_list(request, pk):
    profile=get_object_or_404(Profile, pk=pk)
    followers = profile.followers.all()
    context = {
        'all_user':followers,
    }
    print("followers============",followers)
    return render(request, 'accounts/followers_list.html', context)

@login_required()
def following_list(request, pk):
    profile=get_object_or_404(Profile, pk=pk)
    following = Profile.objects.filter(followers=profile.user)

    context = {
        'all_user':following,
    }
    return render(request, 'accounts/following_list.html', context)


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # print(request.POST.get('connection'))
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)
        profile.save()
        # print(pk,request.user, profile)
        # print("add follower")
        # return HttpResponse("success")

        return redirect('accounts:my_profile', pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # print(request.POST)
        profile = Profile.objects.get(pk=pk)

        profile.followers.remove(request.user)
        profile.save()
        # print(pk,request.user, profile)
        # print("remove follower")
        # return HttpResponse("success")

        return redirect('accounts:my_profile', pk) 

@login_required()
def alluser(request):
    all_user = Profile.objects.order_by('?')
    context = {
        'all_user':all_user,
        
    }
    return render(request, 'accounts/all_user.html', context )


@login_required()
def payment_method_page(request):
    current_customer = request.user.billing
    print("current_customer==========", current_customer)

    # Remove existing card
    if request.method == "POST":
        stripe.PaymentMethod.detach(current_customer.stripe_payment_method_id)
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()
        return redirect(reverse('accounts:payment_method_page'))

    # Save stripe customer infor
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()


    print("stripe_customer_id", current_customer.stripe_customer_id)

    # Get Stripe payment method
    stripe_payment_methods = stripe.PaymentMethod.list(
        customer = current_customer.stripe_customer_id,
        type = "card",
    )

    print("stripe_payment_methods", stripe_payment_methods)

    if stripe_payment_methods and len(stripe_payment_methods.data) > 0:
        payment_method = stripe_payment_methods.data[0]
        current_customer.stripe_payment_method_id = payment_method.id
        current_customer.stripe_card_last4 = payment_method.card.last4
        current_customer.save()
    else:
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()

    if not current_customer.stripe_payment_method_id:
        intent = stripe.SetupIntent.create(
            customer = current_customer.stripe_customer_id
        )

        return render(request, 'accounts/payment_method.html', {
            "client_secret": intent.client_secret,
            "STRIPE_API_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            'brand': stripe_payment_methods['data'][0]['card']['brand'] if len(stripe_payment_methods['data']) >0 else ''
        })
    else:
        return render(request, 'accounts/payment_method.html', {'brand': stripe_payment_methods['data'][0]['card']['brand'] if len(stripe_payment_methods['data']) >0 else ''})


@login_required()
def delete(request, pk):

    if request.method == 'POST':
        for i in request.POST.getlist('id'):

            user = get_object_or_404(User, pk=i)

            team = get_object_or_404(Team, pk=pk)
            team.members.remove(user)


        return redirect('dashboard:teams:team_detail', pk)
 

    return HttpResponse("Something went wrong")



@login_required()
def payout_method_page(request):
    profile = get_object_or_404(Profile, user=request.user)
    payout_form = PayoutForm(instance=profile)

    if request.method == 'POST':
        payout_form = PayoutForm(request.POST, instance=profile)
        if payout_form.is_valid():
            payout_form.save()

            messages.success(request, "Payout address is updated.")
            return redirect(reverse('accounts:account_settings'))

    return render(request, 'accounts/payout_method.html', {
        'payout_form': payout_form
    })
