import json

from datetime import timedelta
from datetime import datetime

import online_users.models

from django.shortcuts import get_object_or_404
from django import template
from django.contrib.auth.models import User


from accounts.models import Profile
from blog.models import Post
from scheme.teams.models import Invitation






from django.db.models import Count



register = template.Library()



@register.filter
def see_users(user):
    print("see_user==============", user)
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    users = (user for user in  user_status)
    active_users = {}
    for i in users:
        active_users[i.user] = i.user.pk
    if user in active_users:
        return True
    return False
   
@register.filter
def delay(datetime_data):
    now = datetime.now().astimezone()
    delay = now-datetime_data
    return delay.days


@register.filter
def query_to_count(entry):
    query_len = []
    for i in entry:
        query_len.append(i.pk)
    return len(query_len)


@register.filter
def query_to_profile(entry):
    query_len = []
    for i in entry:
        query_len.append(i)
    return query_len

@register.filter
def profile_pk(user):
    value = Profile.objects.get(user=user).pk
    return value

@register.filter
def profile_country(user):
    value = Profile.objects.get(user=user).country
    return value

@register.filter
def tojson(params):
    return json.dumps(params)

@register.filter
def profile_state(user):
    value = Profile.objects.get(user=user).state
    return value

@register.filter
def profile_pic(user):
    value = Profile.objects.get(user=user).profile_pic
    return value

@register.filter
def get_email(user):
    value = User.objects.get(username=user).email
    return value

@register.simple_tag
def is_following(author, user):
    profile=get_object_or_404(Profile, user=user)
    print(profile)
    followers = profile.followers.all()
    followers_lst = [i.username for i in followers]
    print(followers_lst, "author=",author)
    if str(author) in followers_lst:
        return True
    print("is_following=============", author in followers_lst)
    return False



@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
        ).order_by('-total_comments')[:count]

@register.simple_tag
def invitations_check(request):
    invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)
    return invitations
