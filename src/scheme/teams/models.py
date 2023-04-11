import uuid

from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    #status
    ACTIVE = 'active'
    DELETED = 'deleted'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    )
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, related_name='created_teams', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)

    class Meta:
        ordering = ['title']
        unique_together = ('title', 'created_by') 
    
    def __str__(self):
        return self.title



class Invitation(models.Model):
    #
    # Status

    INVITED = 'invited'
    ACCEPTED = 'accepted'

    CHOICES_STATUS = (
        (INVITED, 'Invited'),
        (ACCEPTED, 'Accepted')
    )

    team = models.ForeignKey(Team, related_name='invitations', on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=INVITED)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
