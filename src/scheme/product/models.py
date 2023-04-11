# Create your models here.
import uuid

from hitcount.models import HitCountMixin, HitCount
from ckeditor_uploader.fields import RichTextUploadingField 
from taggit.managers import TaggableManager

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from scheme.projects.models import Project


# Create your models here.
class Product(models.Model, HitCountMixin):
    STATUS_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private')
    )

    id = models.UUIDField(primary_key = True, default = uuid.uuid4,editable = False, db_index=True)
    profile_pic = models.ImageField(upload_to='product/profile/%Y/%m/%d/')
    banner_pic = models.ImageField(upload_to='product/banner/%Y/%m/%d/')
    product_name = models.CharField(max_length=256, db_index=True)
    description = models.TextField()
    manual = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='public', db_index=True)
    index = models.BooleanField(default=False, db_index=True)
    category = models.CharField(max_length=250, default='uncategorized')
    tags = TaggableManager(blank=True) 
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    price_per_request = models.FloatField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name 
  
class ProductComment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="comments")
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
        return ProductComment.objects.filter(parent=self).filter(active=True)
        
    
    
    
  
    

    