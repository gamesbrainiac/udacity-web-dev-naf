# coding=utf-8
import os

import webapp2
import jinja2

from google.appengine.ext import db

# Setting directory for template files
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))


JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)


class Post(db.Model):
    title = db.StringProperty(required=True)
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


# Where all the web-page views are
class HomePage(Handler):

    def get(self):
        return self.render('HomePage.html')


class Blog(Handler):

    def get(self):
        # Getting the top 10 most recent posts
        list_of_posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")[:10]

        return_list = {
            'list_of_posts': list_of_posts,
        }

        return self.render('Blog.html', **return_list)


class NewPost(Handler):

    def get(self):
        return self.render('NewPost.html')

    def post(self):
        title = str(self.request.get('title'))
        content = str(self.request.get('content'))

        if title and content:
            data = Post(title=title, content=content)
            data.put()

            return self.redirect('/blog/%s' % data.key().id())

        error = ''
        if not title:
            error += 'There was no title.'
        if not content:
            error += ' There was no content.'

        return_list = {
            'error': error,
            'title': title,
            'content': content,
        }

        return self.render('NewPost.html', **return_list)


class ParticularPost(Handler):

    def get(self, key_id):
        key = db.Key.from_path('Post', int(key_id))
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
