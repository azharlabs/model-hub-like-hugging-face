import uuid

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from scheme.product.models import Product
from scheme.projects.models import Project
# Create your models here.

# Create our models here.
class Files(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    script_name = models.CharField(max_length=254, db_index=True)
    script_file = models.FileField(upload_to='projects/data/%Y/%m/%d/', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.script_name 

class UpdateFileInfo(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    files = models.ForeignKey(Files, on_delete=models.CASCADE,db_index=True)
    updated_author = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    updated_date = models.DateTimeField(auto_now_add=True)


