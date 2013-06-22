# coding=utf-8
import os

import webapp2
import jinja2

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


########## Where all the web-page views are ####################

class MainPage(Handler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = self.request.cookies.get('visits', 0)  # Basically treating cookies as a set of dictionaries
        self.write('You have visited this site %s number of times' % visits)




# External list to handle our page request
page_list = [
    ('/', MainPage),
]
app = webapp2.WSGIApplication(page_list, debug=True)
