import uuid

from django.db import models
from django.contrib.auth.models import User
from scheme.product.models import Product

# Create your models here.
class Model(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    model_name = models.CharField(max_length=256, db_index=True)
    file_name = models.FileField(upload_to ='models/%Y/%m/%d/')
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name 
  

    
    