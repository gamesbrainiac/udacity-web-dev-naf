# coding=utf-8
import os
import webapp2
import jinja2


# Setting up directory helper functions
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
root = lambda *args: os.path.abspath(os.path.join(BASE_DIR, *args))

TEMPLATE_DIR = root('templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)


# Generic handler to reduce work
class GenericHandler(webapp2.RequestHandler):

    def write(self, *args, **kwargs):
        return self.response.out.write(*args, **kwargs)

    def render_template(self, template, context_data=None, **kwargs):
        if not context_data:
            context_data = {}
        renderer = JINJA_ENV.get_template(template)
        return self.write(renderer.render(context_data, **kwargs))