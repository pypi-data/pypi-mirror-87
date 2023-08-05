import random
import string
import uuid


def random_str(length):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, length))

    return salt


def random_uuid():
    return str(uuid.uuid4()).replace('-', '')
