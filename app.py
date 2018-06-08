"""
server.py
Simple Tornado API for GitHub contributions.
"""
import datetime
import json
import os
from urllib.parse import urlsplit

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from tornado.options import define, options

from bson import json_util
from contributions import (get_contributions_daily, get_contributions_monthly,
                           get_contributions_today, get_contributions_weekly)
from dotenv import load_dotenv
from pymongo import MongoClient


define("port", default=8889, help="run on the given port", type=int)
load_dotenv()


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/gh_contribs')

INTERVALS = (
    ('today', get_contributions_today),
    ('daily', get_contributions_daily),
    ('weekly', get_contributions_weekly),
    ('monthly', get_contributions_monthly)
)


class IndexHandler(tornado.web.RequestHandler):
    """
    Serves the homepage for the project.
    URL: /
    """

    def get(self):
        self.render("index.html", **{})


class StatsHandler(tornado.web.RequestHandler):
    """
    Serves GitHub Contribution data via JSON API.
    URL: /api/stats/<today|daily|weekly|monthly>/<username>/
    """

    def get(self, interval, username):
        try:
            get_data_function = dict(INTERVALS)[interval]
            self.write(get_data_function(username))
        except KeyError:
            self.write(
                f"Could not find feed named '{interval}'.\
                Please try 'today', 'daily', 'weekly', or 'monthly.'")
        except:
            self.write({'error': 'An error has occurred.'})


class ScrapeHandler(tornado.web.RequestHandler):
    """
    Scrapes and saves the results to a MongoDB collection.
    URL: /api/scrape/<username>/
    """

    def _get_db_connection(self):
        parsed = urlsplit(MONGODB_URI)
        db_name = parsed.path[1:]
        db = MongoClient(MONGODB_URI)[db_name]
        if '@' in MONGODB_URI:
            user, password = parsed.netloc.split('@')[0].split(':')
            db.authenticate(user, password)
        return db

    def _fetch_contribs_for_user(self, username):
        db = self._get_db_connection()
        db_contribs = db.users.find_one({"username": username})
        return_json = json.dumps(
            db_contribs, indent=4, default=json_util.default)
        return return_json

    def get(self, username):
        """ Fetch user contribs from MongoDB. """
        return_json = self._fetch_contribs_for_user(username)
        self.write(return_json)
        self.set_header('Content-Type', 'application/json')

    def post(self, username):
        """ Initialize a new user. """
        daily_contribs = get_contributions_daily(username)
        weekly_contribs = get_contributions_weekly(username)
        monthly_contribs = get_contributions_monthly(username)
        now = datetime.datetime.utcnow()
        db = self._get_db_connection()
        db.users.update_one({'username': username}, {
            '$setOnInsert': {
                'insertion_date': now
            },
            '$set': {
                'username': username,
                'daily': daily_contribs['contributions'],
                'weekly': weekly_contribs['contributions'],
                'monthly': monthly_contribs['contributions'],
                'last_updated': now
            }
        }, upsert=True)
        return_json = self._fetch_contribs_for_user(username)
        self.write(return_json)
        self.set_header('Content-Type', 'application/json')


def run_server():
    """ Start Tornado. """
    tornado.options.parse_command_line()
    app = tornado.wsgi.WSGIApplication([
        (r"/$", IndexHandler),
        (r"/api/scrape/(\w+)+/$", ScrapeHandler),
        (r"/api/stats/([daily|weekly|monthly|today]+)/(\w+)+/$", StatsHandler),
    ], **{
        'debug': True,
    })
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(app)
    )
    http_server.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    try:
        io_loop.start()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    print(f"[LISTENING] http://localhost:{options.port}")
    run_server()
