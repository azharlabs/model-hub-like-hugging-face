import uuid
from django.db import models


class Newsletter(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    email = models.EmailField(db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email 


class Contact(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    full_name = models.CharField(max_length=256, db_index=True)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=15, db_index=True)
    detail = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name 