import random
import string


def get_random_pipeline_id():
    alpha_numeric = string.ascii_letters + string.digits
    return ''.join((random.choice(alpha_numeric) for i in range(24)))
