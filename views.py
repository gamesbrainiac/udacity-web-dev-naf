# coding=utf-8

# Importing database module from google app engine
from google.appengine.ext import db

# Getting helper methods and settings from other files
from settings import GenericHandler
from models import BlogPost


# Class for home page
class HomePage(GenericHandler):
    def get(self):
        return self.render_template('HomePage.html')


# Class for blog
class Blog(GenericHandler):
    def get(self):
        blog_posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created_at DESC")[:10]  # Getting latest 10 posts
        return_context = {
            'blog_posts': blog_posts,
        }

        return self.render_template('Blog.html', context_data=return_context)


# Class for handling new posts
class NewPost(GenericHandler):
    def get(self):
        return self.render_template('NewPost.html')

    def post(self):
        title = str(self.request.get('title'))  # Grabbing title from POST data
        content = str(self.request.get('content'))  # Grabbing content from POST data

        # If there is both a title and content in the post object
        if title and content:
            data = BlogPost(title=title, content=content)
            data.put()  # Saves the data

            post = int(data.key().id())  # Getting key to the post

            return self.redirect('/blog/%d' % post)  # Redirecting to post permalink

        error = ''  # Creating an error string to return since there was an input error
        if not title:
            error += 'Title not present. '
        if not content:
            error += 'No Content Present.'

        # Return object for the render_template function, contains all the info
        return_context = {
            'title': title,
            'content': content,
            'error': error,
        }

        return self.render_template('NewPost.html', context_data=return_context)


class Post(GenericHandler):
    def get(self, key_id):

        # Getting key based on integer value
        key = db.Key.from_path('BlogPost', int(key_id))  # <-  # Although, I do not know how this thing exactly works,
                                # ^               ^            # I mean where does the whole Key.from_path() come from?
                                # ^ Model object  ^
                                                # ^ What we are querying

        post = db.get(key)  # Saving the object that we have attained using get()

        # If no object was found
        if not post:
            return self.error(404)

        # Otherwise render template with post the data members
        return self.render_template('Post.html', context_data={
            'post': post,
        })