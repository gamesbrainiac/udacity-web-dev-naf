# coding=utf-8
import hashlib
import hmac
import random
import string

SECRET = 'k=azkb=l&d8c55frpi*4pyqb8a^___bm&h4i!w%1d6cd5d7r#p'


def validate_pw(username, password, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(username, password, salt)


def make_pw_hash(username, password, salt=None):
    if not salt:
        salt = make_salt()

    return hashlib.sha256(username + password + salt).hexdigest() + '|' + salt


def make_salt():
    return string.join(random.choice(string.letters) for _ in xrange(5)).replace(' ', '')


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split('|')[0]
    return val if h == make_secure_val(val) else None


print make_pw_hash('Nafiul', 'Cheese')