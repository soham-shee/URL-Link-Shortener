import string
import random

def generate_short_id(n=7):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))
