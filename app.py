"""
server.py
Simple Tornado API for GitHub contributions.
"""
import os

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from tornado.options import define, options

from contributions import (get_contributions_daily, get_contributions_monthly,
                           get_contributions_today, get_contributions_weekly)
from dotenv import load_dotenv


define("port", default=8889, help="run on the given port", type=int)
load_dotenv()


MONGODB_URI = os.getenv('MONGODB_URI')

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


def run_server():
    """ Start Tornado. """
    tornado.options.parse_command_line()
    app = tornado.wsgi.WSGIApplication([
        (r"/$", IndexHandler),
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
