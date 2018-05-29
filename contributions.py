import datetime

from urllib.request import urlopen
from bs4 import BeautifulSoup

MONTH_FORMAT = '%B'
WEEKDAY_FORMAT = '%A'


def get_contributions_daily(uname, today_only=False):
    """
    Output:
    {'contributions': { '2018-05-27': 0,
                        '2018-05-28': 1,
                        '2018-05-29': 6 }
    'username': 'droxey'}
    """
    rects = _get_contributions_element(uname)
    json = {'contributions': {}}
    for rect in rects:
        data_date = rect.get('data-date')
        json['contributions'][data_date] = int(rect.get('data-count', 0))
    if today_only:
        today = datetime.date.today().strftime("%Y-%m-%d")
        json['contributions'] = {today: json.get(today, 0)}
    json['username'] = uname
    return json


def get_contributions_today(uname):
    """
    Output:
    {'contributions': {'2018-05-29': 0}, 'username': 'droxey'}
    """
    return get_contributions_daily(uname, today_only=True)


def get_contributions_weekly(uname):
    """
    Output:
    {'contributions': { 'Friday': 204,
                        'Monday': 85,
                        'Saturday': 41,
                        'Sunday': 7,
                        'Thursday': 130,
                        'Tuesday': 226,
                        'Wednesday': 202 },
    'username': 'droxey'}
    """
    rects = _get_contributions_element(uname)
    json = _get_weekdays()
    for rect in rects:
        data_date = rect.get('data-date')
        count = int(rect.get('data-count', 0))
        day_of_week = _get_datetime(data_date).strftime(WEEKDAY_FORMAT)
        try:
            json['contributions'][day_of_week] += count
        except KeyError:
            pass

    json['username'] = uname
    return json


def get_contributions_monthly(uname):
    """
    Output:
    {'contributions': { 'April': 32,
                        'August': 33,
                        'December': 76,
                        'February': 98,
                        'January': 77,
                        'July': 65,
                        'June': 63,
                        'March': 25,
                        'May': 216,
                        'November': 104,
                        'October': 32,
                        'September': 74 },
    'username': 'droxey'}
    """

    rects = _get_contributions_element(uname)
    json = _get_months()
    for rect in rects:
        data_date = rect.get('data-date')
        month = _get_datetime(data_date).strftime(MONTH_FORMAT)
        json['contributions'][month] += int(rect.get('data-count', 0))
    json['username'] = uname
    return json


def _get_contributions_element(uname):
    """ Scrape profile page. """
    url = 'https://github.com/' + uname
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    rects = soup.find_all("rect")
    return rects


def _get_datetime(ymd_string):
    """ Convert YYYY-MM-DD to datetime.date(). """
    year, month, day = (int(x) for x in ymd_string.split('-'))
    return datetime.date(year, month, day)


def _get_weekdays():
    """ Generate locale-aware weekdays."""
    week_range = range(1, 8)
    initial = [0 for i in week_range]
    weekdays = [datetime.date(datetime.date.today().year, datetime.date.today().month, i).strftime(WEEKDAY_FORMAT)
                for i in week_range]
    return {'contributions': dict(zip(weekdays, initial))}


def _get_months():
    """ Generate locale-aware months."""
    month_range = range(1, 13)
    initial = [0 for i in month_range]
    months = [datetime.date(datetime.date.today().year, i, 1).strftime(MONTH_FORMAT)
              for i in month_range]
    return {'contributions': dict(zip(months, initial))}
