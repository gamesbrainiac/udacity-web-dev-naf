import os
import webapp2
import jinja2

import ProblemSet2


# Setting up directory helper functions
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
root = lambda *args: os.path.abspath(os.path.join(BASE_DIR, *args))

TEMPLATE_DIR = root('templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)


class GenericHandler(webapp2.RequestHandler):

    def write(self, *args, **kwargs):
        return self.response.out.write(*args, **kwargs)

    def render_template(self, template, context_data=None):
        if not context_data:
            context_data = {}
        renderer = JINJA_ENV.get_template(template)
        return self.write(renderer.render(context_data))


class HomePageHandler(GenericHandler):

    def get(self):
        return self.render_template('home_page.html')


class ThanksHandler(GenericHandler):

    def get(self):
        return self.render_template('thanks.html')


class Rot13(GenericHandler):

    def get(self):
        return self.render_template('rot-13.html', {})

    def post(self):
        text = str(self.request.get('text'))
        return_context = {
            'text': ProblemSet2.rotate_thirteen(text),
        }
        return self.render_template('rot-13.html', return_context)


class SignupHandler(GenericHandler):

    def get(self):
        return self.render_template('signup.html')

    def post(self):
        username = str(self.request.get('username'))
        password = str(self.request.get('password'))
        verify = str(self.request.get('verify'))
        email = str(self.request.get('email'))

        username_error = False
        if not ProblemSet2.validate_username(username):
            username_error = 'Invalid username'

        password_error = False
        if not ProblemSet2.validate_password(password, verify=verify):
            password_error = 'Invalid password'
            password = verify = ''

        email_error = False
        if not ProblemSet2.validate_email(email):
            email_error = 'Invalid E-mail'

        return_context = {
            'username': username,
            'password': password,
            'verify': verify,
            'email': email,
            'password_error': password_error,
            'username_error': username_error,
            'email_error': email_error,
        }

        return_context = {key: value for key, value in return_context.items() if value}

        if not(username_error or password_error or email_error):
            return self.redirect('/thanks')
        else:
            return self.render_template('signup.html', return_context)


page_list = [
    ('/', HomePageHandler),
    ('/unit2/rot13', Rot13),
    ('/unit2/signup', SignupHandler),
    ('/thanks', ThanksHandler)
]
app = webapp2.WSGIApplication(page_list, debug=True)
