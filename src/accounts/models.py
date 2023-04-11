import uuid

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/%Y/%m/%d/')
    banner_pic = models.ImageField(upload_to='banner_pic/%Y/%m/%d/')
    profile_privacy = models.CharField(max_length=25, db_index=True, default='anyone')
    phone = models.CharField(max_length=15, db_index=True)
    company = models.CharField(max_length=256, db_index=True)
    first_name = models.CharField(max_length=256, db_index=True)
    last_name = models.CharField(max_length=256, db_index=True)
    account_type = models.CharField(max_length=256, db_index=True)
    country = models.CharField(max_length=256, db_index=True)
    city = models.CharField(max_length=256, db_index=True)
    state = models.CharField(max_length=256, db_index=True)
    address1 = models.CharField(max_length=256, db_index=True)
    address2 = models.CharField(max_length=256, db_index=True)
    zip_code = models.CharField(max_length=256, db_index=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    paypal_email = models.EmailField(max_length=255, blank=True, db_index=True)


    def __str__(self):
        return self.user.username


class Preferences(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    early_release = models.BooleanField(default=True)
    profile_viewed = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_people"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_people"
    )

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}"


class Billing(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payment_method_id = models.CharField(max_length=255, blank=True)
    stripe_card_last4 = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username