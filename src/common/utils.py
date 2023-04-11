import random
import string
from django.core.exceptions import ValidationError
from django.http import HttpResponse



def get_random_password(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return result_str




def validate_file(value):
    value= str(value)
    print(value.endswith(".csv"))
    if value.endswith(".csv") != True: 
        return False
    return True


def validate_pickle_file(value):
    value= str(value)
    print(value.endswith(".pkl"))
    if value.endswith(".pkl") != True: 
        return False
    return True