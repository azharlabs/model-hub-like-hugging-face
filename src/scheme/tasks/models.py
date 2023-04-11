from django.db import models
from django.contrib.auth.models import User

from scheme.teams.models import Team
from scheme.projects.models import Project


class Task(models.Model):
    #
    # Status choices

    TODO = 'todo'
    DONE = 'done'
    ARCHIVED = 'archived'

    CHOICES_STATUS = (
        (TODO, 'Todo'),
        (DONE, 'Done'),
        (ARCHIVED, 'Archived')
    )

    team = models.ForeignKey(Team, related_name='tasks', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=TODO)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title