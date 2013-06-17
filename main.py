import webapp2

form = """
<!doctype html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <form action="" method="POST">
        What is your birthday
        <br>
        <label>
            Day:
            <input type="text" name="day" value="%(day)s"/>
        </label>
        <br>
        <label>
            Month:
            <input type="text" name="month" value="%(month)s"/>
        </label>
        <br>
        <label>
            Year
            <input type="text" name="year" value="%(year)s"/>
        </label>
        <div style="color: red">%(error)s</div>
        <br>
        <br>
        <input type="submit"/>
    </form>
</body>
</html>
"""

# In method, it does not matter if you write it in upper or
# lower case, both 'post' and 'POST' will work.
# When submitting data, always use POST

from test_functions import *


class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {'error': error,
                                        'month': month,
                                        'day': day,
                                        'year': year, })

    def get(self):
        # This line below sets content to text/plain
        # Meaning that it will print out nothing but
        # plain text, so no HTML is rendered
        # self.response.headers['Content-Type'] = 'text/plain'   # Uncomment to see effects of above comments
        self.write_form()

    def post(self):
        user_day = self.request.get("day")
        user_month = self.request.get("month")
        user_year = self.request.get("year")

        month = validate_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form(error="Input invalid",
                            month=month,
                            day=day,
                            year=year)
        else:
            return self.response.out.write("Thanks for the form man! :D")


# class TestHandler(webapp2.RedirectHandler):
#     # This defines what happens when a GET request is sent to the server
#     def get(self):
#         q = self.request.get("q")
#         self.response.write(q)
#
#     def post(self):
#         self.response.headers['Content-Type'] = 'text/plain'  # Sets content to text/plain
#         self.response.out.write(self.request)                 # Prints out the entire request
#         # q = self.request.get("q")
#         # self.response.write(q)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
