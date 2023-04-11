import uuid

from django.db import models
from django.contrib.auth.models import User

from scheme.teams.models import Team


# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    project_name = models.CharField(max_length=256, db_index=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project')
    image = models.ImageField(upload_to='projects/%Y/%m/%d/')
    description = models.TextField()
    client_name = models.CharField(max_length=256, db_index=True, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name 

    def num_tasks_todo(self):
        return self.tasks.filter(status=Task.TODO).count()