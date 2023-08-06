import string
import random


def generate_random_str(num=4):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits
    ) for _ in range(num))


def price_beautifier(amount):
    try:
        return "{:,}".format(int(amount))
    except:
        return amount
