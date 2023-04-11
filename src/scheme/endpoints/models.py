# Create your models here.
import uuid

from django.db import models
from scheme.product.models import Product


# Create your models here.
class endPoint(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    endpoint_file = models.FileField(upload_to='endpoint/%Y/%m/%d/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name
 
  
    