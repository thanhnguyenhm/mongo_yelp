import random
import string


def random_rating_id(length=22):
    st = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.sample(st, length))

# Need to decide if we should use static variable with fix value or generate user id for every session
# def random_user_id(length=22):
#     st = string.ascii_lowercase + string.digits + string.ascii_uppercase
#     return ''.join(random.sample(st, length))