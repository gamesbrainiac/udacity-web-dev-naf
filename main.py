import webapp2

import ProblemSet2

form = """
<!doctype html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title>Testing Grounds</title>
</head>
<body>
    <h2>
        Welcome to ROT13
    </h2>
    <form action="" method="post">
        <label>
            <textarea name="text" id="rot-13-textbox" cols="100" rows="10">%(text_to_render)s</textarea>
            <br>
            <input type="submit"/>
        </label>
    </form>
</body>
</html>
"""

signup_form = """
<!doctype html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title>Testing Grounds</title>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">
</head>
<body>
    <div class="container" style="padding: 20px">
        <h2>
            Sign Up! :D
        </h2>
        <form action="" method="post">
            <label for="Name">
                Username:
                <input type="text" name="username" value="%(username)s" />
            </label>
            <div style="color: red">
                %(error_user)s
            </div>
            <label for="Password">
                Password:
                <input type="text" name="password" value="%(password)s" />
            </label>
            <div style="color: red">
                %(error_password)s
            </div>
            <label for="Verification">
                Verify Password:
                <input type="text" name="verify" value="%(verify)s" />
            </label>
            <label for="E-mail">
                E-mail: (optional)
                <input type="text" name="email" value="%(email)s" />
            </label>
            <div style="color: red">
                %(error_email)s
            </div>
            <input type="submit"/>
        </form>
    </div>
    <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
</body>
</html>
"""

thanks_form = """
<!doctype html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title>Testing Grounds</title>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">
</head>
<body>
    <div class="container" style="padding: 20px">
        <h1>
            Thanks %(username)s
        </h1>
    </div>
    <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
</body>
</html>
"""

#### GENERIC HANDLERS


# Creating a generic class to manage input and output
class GenericHandler(webapp2.RequestHandler):
    def write(self, html=''):
        self.response.out.write(html)


#### Main Views
class SignupHandler(GenericHandler):

    def get(self):
        self.write(signup_form % {
            'username': '',
            'password': '',
            'verify': '',
            'email': '',
            'error_user': '',
            'error_password': '',
            'error_email': '',
        })

    def post(self):

        # Getting all input

        user_input = {
            'username': self.request.get('username'),
            'password': self.request.get('password'),
            'verify': self.request.get('verify'),
            'email': self.request.get('email'),
        }

        # Verification process begins
        # -> Verifying username
        username = True
        if not ProblemSet2.validate_username(user_input['username']):
            user_input['error_user'] = 'Invalid Username'
            username = False
        else:
            user_input['error_user'] = ''

        # -> Verifying password
        password = True
        if not ProblemSet2.validate_password(user_input['password']):
            user_input['error_password'] = 'Invalid Password'
            if user_input['password'] != user_input['verify']:
                user_input['password'] = user_input['verify'] = ''
                user_input['error_password'] += ' and passwords do not match'
            password = False
        else:
            user_input['error_password'] = ''

        email = True
        if email != '':
            if not ProblemSet2.validate_email(user_input['email']):
                user_input['error_email'] = 'Invalid email address'
                email = False
            else:
                user_input['error_email'] = ''
        else:
            user_input['error_email'] = ''

        if username and password and email:
            return self.redirect('/thanks')
        else:
            print user_input
            return self.write(signup_form % user_input)


class ThanksHandler(GenericHandler):
    def get(self):
        return self.write(thanks_form)


class RotThirteenHandler(GenericHandler):
    def get(self):
        return self.write(form)

    def post(self):
        text = str(self.request.get('text'))
        text = ProblemSet2.rotate_thirteen(text)
        text = ProblemSet2.escape_html(text)

        post_form = form % {
            'text_to_render': text,
        }

        return self.write(post_form)


# Main page
class MainHandler(GenericHandler):
    def get(self):
        return self.write('Hello World')

page_list = [
    ('/', MainHandler),
    ('/rot13', RotThirteenHandler),
    ('/signup', SignupHandler),
    ('/thanks', ThanksHandler),
]
app = webapp2.WSGIApplication(page_list, debug=True)
