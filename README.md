# api-contrib-tornado

Using Tornado + BeautifulSoup to asynchronously scrape daily, weekly, and monthly GitHub contribution statistics from a user's GitHub profile page.

## Test URLs:

* **TODAY**: [https://api-contrib-tornado.herokuapp.com/api/stats/today/droxey/](https://api-contrib-tornado.herokuapp.com/api/stats/today/droxey/)
* **DAILY**: [https://api-contrib-tornado.herokuapp.com/api/stats/daily/droxey/](https://api-contrib-tornado.herokuapp.com/api/stats/daily/droxey/)
* **WEEKLY**: [https://api-contrib-tornado.herokuapp.com/api/stats/weekly/droxey/](https://api-contrib-tornado.herokuapp.com/api/stats/weekly/droxey/)
* **MONTHLY**: [https://api-contrib-tornado.herokuapp.com/api/stats/monthly/droxey/](https://api-contrib-tornado.herokuapp.com/api/stats/monthly/droxey/)

## Installation

1. `git clone git@github.com:outputs-io/api-contrib-tornado`
1. `cd api-contrib-tornado`
1. `pipenv install`
1. `pipenv shell`
1. `python app.py`

### Special Thanks

 `contributions.py` based upon a solution by [Chris Yunbin Chang](https://github.com/Yunbin-Chang) for his [GitHub Contributions API](https://github.com/Yunbin-Chang/Github-Contributions-API) project.
