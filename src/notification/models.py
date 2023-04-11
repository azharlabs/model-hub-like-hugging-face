import uuid 

from django.db import models
from django.contrib.auth.models import User

class EmailNotification(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_update = models.BooleanField(default=True)
    interested_blog_update = models.BooleanField(default=True)
    new_device_signin = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

