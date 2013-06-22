# coding=utf-8
import os

import webapp2
import jinja2

from google.appengine.ext import db

# Setting directory for template files
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

# Creating the jinja environment
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)


class PostModel(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)

    def render(self):
        return str(self.content).replace('\n', '<br>')


# Creating generic page handler class
class Handler(webapp2.RequestHandler):

    def write(self, *args, **kwargs):
        return self.response.out.write(*args, **kwargs)

    def render(self, template, **kwargs):
        template = JINJA_ENV.get_template(template)
        return self.write(template.render(**kwargs))


########## Where all the web-page views are ####################

# The homepage view
class HomePage(Handler):

    def get(self):
        return self.render('HomePage.html')


# view for our blog roll
class Blog(Handler):

    def get(self):
        # Getting the top 10 most recent posts
        list_of_posts = PostModel.all().order("-created")[:10]

        return_list = {
            'list_of_posts': list_of_posts,
        }

        return self.render('Blog.html', **return_list)


# View for creating a new post
class NewPost(Handler):

    def get(self):
        return self.render('NewPost.html')

    def post(self):
        subject = str(self.request.get('subject'))
        content = str(self.request.get('content'))

        if subject and content:
            data = PostModel(subject=subject, content=content)
            data.put()

            return self.redirect('/blog/%s' % data.key().id())

        error = ''
        if not subject:
            error += 'There was no subject.'
        if not content:
            error += ' There was no content.'

        return_list = {
            'error': error,
            'subject': subject,
            'content': content,
        }

        return self.render('NewPost.html', **return_list)


# View for going to a particular post
class ParticularPost(Handler):

    def get(self, key_id):
        key = db.Key.from_path('PostModel', int(key_id))
        post = db.get(key)

        return_list = {
            'post': post,
        }

        return self.render('ParticularPost.html', **return_list)


# External list to handle our page request
page_list = [
    ('/', HomePage),
    ('/blog', Blog),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', ParticularPost)
]
app = webapp2.WSGIApplication(page_list, debug=True)
