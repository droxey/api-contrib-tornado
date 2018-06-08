# api-contrib-tornado

Using Tornado + BeautifulSoup to scrape daily, weekly, and monthly GitHub contribution statistics from a user's GitHub profile page.

Deployable on Heroku and Dokku!

## Test URLs

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

## Deployment via Heroku

1. `heroku login`
1. `heroku create my-app-name --stack=cedar`
1. `heroku addons:create mongolab`
1. `heroku config:add TZ="UTC"`
1. `git add . && git commit -m "[deploy] Pushing to Heroku."`
1. `git push heroku master`
1. `heroku ps:scale web=1`

## Deployment via Dokku

1. On your remote Dokku host, run `dokku apps:create contrib-api`.
1. In your local repo, run `git remote add dokku ssh://dokku@YOUR_DOKKU_URL/contrib-api` to add the new remote.
1. Deploy by running `git push dokku master`.

### Special Thanks

 `contributions.py` based upon a solution by [Chris Yunbin Chang](https://github.com/Yunbin-Chang) for his [GitHub Contributions API](https://github.com/Yunbin-Chang/Github-Contributions-API) project.
