__author__ = 'Nafiul Islam'


# coding=utf-8
import hashlib


def hash_str(s):
    return hashlib.md5(s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split('|')[0]
    return val if h == make_secure_val(val) else None
