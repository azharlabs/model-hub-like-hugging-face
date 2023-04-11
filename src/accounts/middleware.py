from .models import Profile, Preferences, Billing
from notification.models import EmailNotification
from membership.models import Customer


class ProfileMiddlware:
  def __init__(self, get_response):
    self.get_response = get_response
    # One-time configuration and initialization.

  def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
    if request.user.is_authenticated and not Profile.objects.filter(user=request.user).exists():
        Profile.objects.create(user=request.user)

    if request.user.is_authenticated and not Preferences.objects.filter(user=request.user).exists():
        Preferences.objects.create(user=request.user)

    if request.user.is_authenticated and not EmailNotification.objects.filter(user=request.user).exists():
        EmailNotification.objects.create(user=request.user)

    if request.user.is_authenticated and not Customer.objects.filter(user=request.user).exists():
        Customer.objects.create(user=request.user)

    if request.user.is_authenticated and not Billing.objects.filter(user=request.user).exists():
        Billing.objects.create(user=request.user)

    response = self.get_response(request)

    # Code to be executed for each request/response after
    # the view is called.

    return response