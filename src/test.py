import re
 
# Define a function for
# for validating an Email
def check_email(email):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(pat,email):
        print("Valid Email")
    else:
        print("Invalid Email")


# Driver Code
if __name__ == '__main__':
 
    # Enter the email
    email = "ankitrai326@gmail.com"
 
    # calling run function
    check_email(email)
 
    email = "my.ownsite@our-earth.org"
    check_email(email)
 
    email = "ankitrai326.com"
    check_email(email)