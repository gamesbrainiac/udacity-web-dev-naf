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

from test_functions import *


class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {'error': error,
                                        'month': escape_html(month),
                                        'day': escape_html(day),
                                        'year': escape_html(year), })

    def get(self):
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
                            month=user_month,
                            day=user_day,
                            year=user_year)
        else:
            return self.redirect('/thanks', )


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        return self.response.out.write("Thanks for the form man! :D")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
