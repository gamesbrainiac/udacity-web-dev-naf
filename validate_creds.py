# coding=utf-8
import re


def validate_username(username=''):
    USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    return USER_RE.match(username)


def validate_password(password='', verify=''):
    PASS_RE = re.compile(r'^.{3,20}$')
    return verify == password and PASS_RE.match(password)


def validate_email(email=''):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return True if not email else EMAIL_RE.match(email)