import random


def random_salt():
    return ''.join(random.choice('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789!#$()?@[]')
                   for i in range(16))
