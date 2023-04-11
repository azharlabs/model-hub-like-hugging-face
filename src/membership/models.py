from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False,db_index=True)
    membership = models.BooleanField(default=False, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)