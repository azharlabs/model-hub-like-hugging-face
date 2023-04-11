import stripe


from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponse


from .models import Customer


stripe.api_key = settings.STRIPE_SECRET_KEY



@login_required
def member_settings(request):
    membership = False
    cancel_at_period_end = False
    #ads
 

    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return redirect('accounts:account_settings') #render(request, 'membership/settings.html', {'membership':membership,
    # 'cancel_at_period_end':cancel_at_period_end,
    # })


def join(request):
    #ads
   
    context = {
 
    }
    return render(request, 'membership/join.html', context)


def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = get_object_or_404(Customer, user = request.user)
       
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()
    return redirect('accounts:account_settings') #render(request, 'membership/success.html')


def cancel(request):
    return render(request, 'membership/cancel.html')


@login_required
def checkout(request):

    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 10
        membership_id = 'price_1JM7Z2GQMhYolRJEUrwXR9An'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1JM7ZuGQMhYolRJELM6YUPdR'
                final_dollar = 25

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/m/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/m/cancel',
        )

        context = {
            'final_dollar': final_dollar,
            'session_id': session.id, 
            'public_key':settings.STRIPE_PUBLIC_KEY

        }

        return render(request, 'membership/checkout.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')