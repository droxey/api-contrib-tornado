import datetime

from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_contributions_daily(uname, today_only=False):
    """
    Output:
    [{"date" : "2017-02-27",  "count" : "2"}, {"date" : "2017-02-28", "count" : "10"}]
    """
    rects = get_contributions_element(uname)
    json = {'contributions': []}
    for rect in rects:
        data_date = rect.get('data-date')
        data_count = int(rect.get('data-count', 0))
        json['contributions'].append({'date': data_date, 'count': data_count})
    if today_only:
        today_contribs = {'contributions': []}
        today_contribs['contributions'].append(json['contributions'][-1])
        json = today_contribs
    return json


def get_contributions_today(uname):
    """
    Output: {"contributions": [{"date": "2018-05-29", "count": 5}]}
    """
    return get_contributions_daily(uname, today_only=True)


def get_contributions_weekly(uname):
    """
    Output:
    { "Sunday": "50", "Monday": "25", "Tuesday": "57",
      "Wednesday": "33", "Thursday": "14", "Friday": "15", "Saturday": "18" }
    """
    rects = get_contributions_element(uname)
    json = {
        'Sunday': 0,
        'Monday': 0,
        'Tuesday': 0,
        'Wednesday': 0,
        'Thursday': 0,
        'Friday': 0,
        'Saturday': 0
    }
    for rect in rects:
        data_date = rect.get('data-date')
        count = int(rect.get('data-count'))
        year, month, day = (int(x) for x in data_date.split('-'))
        ans = datetime.date(year, month, day)
        day_of_week = ans.strftime("%A")
        json[day_of_week] += count
    return json


def get_contributions_monthly(uname):
    """
    Output:
    { "01" : "58", "02" : "102", "03" : "16", "04" : "0",
      "05" : "0", "06" : "0", "07" : "2","08" : "6","09" : "0",
      "10" : "8", "11" : "17", "12" : "10" }
    """

    rects = get_contributions_element(uname)
    json = {
        '01': 0,
        '02': 0,
        '03': 0,
        '04': 0,
        '05': 0,
        '06': 0,
        '07': 0,
        '08': 0,
        '09': 0,
        '10': 0,
        '11': 0,
        '12': 0
    }
    for rect in rects:
        data_date = rect.get('data-date')
        month = data_date.split('-')[1]
        json[month] += int(rect.get('data-count', 0))
    return json


def get_contributions_element(uname):
    """ Scrape profile page. """
    url = 'https://github.com/' + uname
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    rects = soup.find_all("rect")
    return rects
