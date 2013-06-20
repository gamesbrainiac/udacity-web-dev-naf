import os
import webapp2
import jinja2

from google.appengine.ext import db


# Setting up directory helper functions
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
root = lambda *args: os.path.abspath(os.path.join(BASE_DIR, *args))

TEMPLATE_DIR = root('templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class GenericHandler(webapp2.RequestHandler):

    def write(self, *args, **kwargs):
        return self.response.out.write(*args, **kwargs)

    def render_template(self, template, context_data=None, **kwargs):
        if not context_data:
            context_data = {}
        renderer = JINJA_ENV.get_template(template)
        return self.write(renderer.render(context_data, **kwargs))


class HomePageHandler(GenericHandler):

    def render_page(self, context_data=None, **kwargs):
        art_works = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

        return self.render_template('home_page.html', context_data=context_data, listOfArt=art_works, **kwargs)

    def get(self):
        return self.render_page()

    def post(self):
        title = str(self.request.get('title'))
        art = str(self.request.get('art'))

        if title and art:
            a = Art(title=title, art=art)
            a.put()

            return self.redirect('/')
        else:
            return_data = {
                'error': 'We need both a title and art-work man! :(',
                'art': art,
                'title': title,
            }
            return self.render_page(context_data=return_data)


page_list = [
    ('/', HomePageHandler),
]
app = webapp2.WSGIApplication(page_list, debug=True)
