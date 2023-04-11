# Create your models here.
import uuid

from django.db import models
from django.contrib.auth.models import User
from scheme.projects.models import Project
from scheme.model.models import Model
from scheme.scripts.models import Scripts

# Create your models here.
class Fields(models.Model):
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'float'


    CHOICES_TYPE = (
        (STRING, 'string'),
        (INTEGER, 'integer'),
        (FLOAT, 'float')

    )

    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    field_name = models.CharField(max_length=256, db_index=True)
    field_type = models.CharField(max_length=20, choices=CHOICES_TYPE, default=STRING)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    scripts = models.ForeignKey(Scripts, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.field_name 
  
    

    