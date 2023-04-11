import uuid

from django.db import models
from django.contrib.auth.models import User

from scheme.files.models import Files


class pandasCode(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    pandas_code = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    model_type = models.CharField(max_length=120, db_index=True, blank=True)
    data = models.ForeignKey(Files, on_delete=models.CASCADE, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)


    def __str__(self):
        return self.data.script_name 
  