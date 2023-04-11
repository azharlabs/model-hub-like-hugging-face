


def see_users(pk):
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    users = (user for user in  user_status)
    for i in users:
        online_users[i.user.pk] = i.user
    if pk in online_users:
        return True
    return False
   