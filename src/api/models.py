import uuid

from django.db import models
from django.contrib.auth.models import User
from scheme.teams.models import Team
from scheme.product.models import Product


# Create your models here.
class API(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    api = models.CharField(max_length=256, db_index=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api', db_index=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, db_index=True)
    enddate = models.DateTimeField(blank=True, null=True, db_index=True)
    

    def __str__(self):
        return self.user.username



class apiLog(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    api = models.ForeignKey(API, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ('-created_date',)


class apiplayLog(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    price = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.product_name
