from random import choice
from datetime import datetime, timedelta
import uuid
import string

ACCESS_KEY_LENGTH = 64
EXPIRED_HOURS = 24


def generate_id():
    return uuid.uuid4().bytes


def str_id_to_bytes(str_id):
    return uuid.UUID(str_id).bytes


def bytes_id_to_str(bytes_id):
    return str(uuid.UUID(bytes=bytes_id))


def generate_token(length=ACCESS_KEY_LENGTH):
    simbols = string.ascii_letters + string.digits + '!#$%&*+-<=>?@'
    return ''.join(choice(simbols) for i in range(length))


def get_expired(hours=EXPIRED_HOURS, days=0):
    return datetime.utcnow() + timedelta(hours=hours, days=days)