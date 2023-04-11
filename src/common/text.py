welcome_message = """

Hi {username}, 

Thank you for registering in {SITE_NAME},
username = {username},
password = {password}

Don't share this with anyone. if password is misssed please use forgot password feature.

Thanks,
{SITE_OWNER}


"""

enquiry_message = """

Hi admin team, 

We received one enquiry from user. please reply as soon as possible.

information:-

fullname = {fullname},
email = {email},
phone = {phone}
detail = {detail}

Don't share this with anyone. this is confidential. 

(this is system generated mail)

Thanks,
{SITE_OWNER}


"""

email_message_changed = """

Hi {username}, 

email address changed. this is email address is not valid anymore for this account.

account url = {account_url}
changed email address = {new_email}

Don't share this with anyone. this is confidential. 

(this is system generated mail)

Thanks,
{SITE_OWNER}

"""