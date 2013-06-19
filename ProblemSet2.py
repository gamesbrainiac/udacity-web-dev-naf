import string
import re


def rotate_thirteen(input_string=''):
    rot13 = string.maketrans(
        'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
        'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
    return string.translate(input_string, rot13)


def validate_username(username=''):
    USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    return USER_RE.match(username)


def validate_password(password='', verify=''):
    PASS_RE = re.compile(r'^.{3,20}$')
    return verify == password and PASS_RE.match(password)


def validate_email(email=''):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    if not email:
        return True
    else:
        return EMAIL_RE.match(email)