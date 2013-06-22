# coding=utf-8
import os

import webapp2
import jinja2

import security

# Setting directory for template files
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

# Creating the jinja environment
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)


# Creating generic page handler class
class Handler(webapp2.RequestHandler):

    def write(self, *args, **kwargs):
        return self.response.out.write(*args, **kwargs)

    def render(self, template, **kwargs):
        template = JINJA_ENV.get_template(template)
        return self.write(template.render(**kwargs))


class MainPage(Handler):

    def get(self):
        # Setting content type to text
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


# External list to handle our page request
page_list = [
    ('/', MainPage)
]
app = webapp2.WSGIApplication(page_list, debug=True)
