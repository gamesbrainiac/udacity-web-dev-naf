# coding=utf-8
import os

import webapp2
import jinja2
from google.appengine.ext import db

import security
from validate_creds import *

# Setting directory for template files
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

# Creating the jinja environment
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)


class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(default='')


# Creating generic page handler class
class Handler(webapp2.RequestHandler):

    # Simply a cover function to make things faster and more legible
    def write(self, *args, **kwargs):
        return self.response.out.write(*args, **kwargs)

    # Renders template, with HTML file and named arguments
    def render(self, template, **kwargs):
        template = JINJA_ENV.get_template(template)
        return self.write(template.render(**kwargs))


class MainPage(Handler):

    # Basig get function for any GET request from the user
    def get(self):
        # Setting content type to text/plain, for visibility
        self.response.headers['Content-Type'] = 'text/plain'

        visits = 0  # Settings default value

        # Looking up cookie
        visit_cookie_str = self.request.cookies.get('visits')  # Treats cookies like a python dict

        # If we have a cookie
        if visit_cookie_str:
            # We validate it
            cookie_val = security.check_secure_val(visit_cookie_str)
            # If validated
            if cookie_val:
                visits = int(cookie_val)

        # Incrementing cookie value
        visits += 1

        new_cookie_val = security.make_secure_val(str(visits))

        # Writing the cookie down
        # We are using add_header here
        # because we do not want to over
        # -write any other headers with
        # the same name
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)

        if visits > 10000:
            self.write("You are the best evvaahh! :D")
        else:
            self.write("You have visited this page %s times" % visits)


class SignupPage(Handler):

    # Rendering basic login page
    def get(self):
        return self.render('SignupPage.html')

    def post(self):
        # Take in all user input
        username = str(self.request.get('username'))
        password = str(self.request.get('password'))
        verify = str(self.request.get('verify'))
        email = str(self.request.get('email'))

        # Validate things
        error = ''
        if not validate_username(username):
            error += 'Invalid username. '

        if not validate_password(password, verify):
            error += 'Invalid password or passwords do not match. '

        if not validate_email(email):
            error += 'Invalid email.'

        # All things good, then we head for making cookies otherwise, re-render page
        if error == '':
            users = db.GqlQuery("SELECT * FROM User")  # Getting all users
            user = None  # Setting default to None, because that means that we can add this user

            # Looping through users
            for var in users:
                if var.username == username:
                    user = username

            # If there was another user with the same username
            if user:

                # Render back the page, with an error
                return self.render('SignupPage.html',
                                   username=username,
                                   email=email,
                                   error='Username already exists')
            else:  # If user does not exist

                # Making a cookie from username and password
                auth_cookie_str = security.make_pw_hash(username, password)

                # save the username and hash to the database, as well as the email
                new_user = User(username=username, password=auth_cookie_str, email=email)
                new_user.put()

            # Adding cookie headers for re-direct
            self.response.headers.add_header('Set-Cookie', 'auth=%s;Path=/' % auth_cookie_str)
            self.response.headers.add_header('Set-Cookie', 'name=%s;Path=/' % username)
            return self.redirect('/welcome')
        else:
            return self.render('SignupPage.html',
                               username=username,
                               email=email,
                               error=error, )


class LoginPage(Handler):

    def get(self):
        return self.render('LoginPage.html')

    def post(self):
        username = str(self.request.get('username'))
        password = str(self.request.get('password'))

        users = db.GqlQuery("SELECT * FROM User")

        hash_value = None

        for var in users:
            if var.username == username:
                hash_value = var.password

        if hash_value:
            if security.validate_pw(username, password, hash_value):
                self.response.headers.add_header('Set-Cookie', 'auth=%s;Path=/' % str(hash_value))
                self.response.headers.add_header('Set-Cookie', 'name=%s;Path=/' % str(username))
                return self.redirect('/welcome')
        else:
            return self.render('LoginPage.html',
                               username=username,
                               password='',
                               error='Username invalid',)


class LogoutPage(Handler):

    def get(self):
        self.response.headers.add_header('Set-Cookie', 'auth=%s;Path=/' % '')
        self.response.headers.add_header('Set-Cookie', 'name=%s;Path=/' % '')
        return self.redirect('/signup')


class WelcomePage(Handler):

    def get(self):
        # Getting the name cookie
        name_cookie_str = self.request.cookies.get('name')  # TODO: Change the way the username is take in

        # If we could get a name cookie
        if name_cookie_str:
            name_cookie_val = str(name_cookie_str)
            return self.render('WelcomePage.html', username=name_cookie_val)
        # Otherwise, the person is not a valid user <<< Possible use of database here.
        else:
            return self.redirect('/signup')


# External list to handle our page request (looks prettier)
page_list = [
    ('/', MainPage),
    ('/login', LoginPage),
    ('/signup', SignupPage),
    ('/welcome', WelcomePage),
    ('/logout', LogoutPage),
]
app = webapp2.WSGIApplication(page_list, debug=True)
