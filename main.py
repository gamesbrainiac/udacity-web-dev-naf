# coding=utf-8
import webapp2

from views import *

page_list = [
    ('/', HomePage),
    ('/blog/?', Blog),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', Post),
]
app = webapp2.WSGIApplication(page_list, debug=True)
