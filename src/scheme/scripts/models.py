# Create your models here.
import uuid

from django.db import models
from django.contrib.auth.models import User
from scheme.product.models import Product
from django.urls import reverse

# Create your models here.
class Scripts(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    script_code = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    def get_absolute_url(self):
        return reverse('dashboard:scripts:script_detail',args=[self.id])

    def __str__(self):
        return self.product.product_name 
  

class UpdateScriptInfo(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    scripts = models.ForeignKey(Scripts, on_delete=models.CASCADE,db_index=True)
    updated_author = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    updated_date = models.DateTimeField(auto_now_add=True)


class ScriptComment(models.Model):
    script=models.ForeignKey(Scripts,on_delete=models.CASCADE, related_name="comments")
    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
    def get_comments(self):
        return ScriptComment.objects.filter(parent=self).filter(active=True)
        