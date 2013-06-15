import webapp2

form = """
<!doctype html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<form action="/testform" method="POST">
    <input name="q" />
    <input type="submit"/>
</form>
</body>
</html>
"""

# In method, it does not matter if you write it in upper or
# lower case, both 'post' and 'POST' will work.


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # This line below sets content to text/plain
        # Meaning that it will print out nothing but
        # plain text, so no HTML is rendered
        # self.response.headers['Content-Type'] = 'text/plain'   # Uncomment to see effects of above comments
        self.response.write(form)


class TestHandler(webapp2.RedirectHandler):
    # This defines what happens when a GET request is sent to the server
    def get(self):
        q = self.request.get("q")
        self.response.write(q)

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'  # Sets content to text/plain
        self.response.out.write(self.request)                 # Prints out the entire request
        # q = self.request.get("q")
        # self.response.write(q)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/testform', TestHandler),
], debug=True)
