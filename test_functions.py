import datetime
import cgi


def valid_day(day=""):
    # assert isinstance(day, str)
    if day.isdigit():
        day = int(day)
        if 1 <= day <= 31:
            return day
        else:
            return None
    return None


def validate_month(month=""):
    if month.isdigit():
        month = int(month)
        if 1 <= month <= 12:
            return month
    return None


def valid_year(year=""):
    if year.isdigit():
        year = int(year)
        if 1900 <= year <= datetime.datetime.now().year:
            return year
    return None


def escape_html(s=''):
    if s:
        return cgi.escape(s, quote=True)