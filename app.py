"""
server.py
Simple Tornado API for GitHub contributions.
"""
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.autoreload
import tornado.wsgi
from tornado.options import define, options

from contributions import get_contributions_daily, \
    get_contributions_weekly, get_contributions_monthly, \
    get_contributions_today


INTERVALS = (
    ('today', get_contributions_today),
    ('daily', get_contributions_daily),
    ('weekly', get_contributions_weekly),
    ('monthly', get_contributions_monthly)
)

define("port", default=8888, help="run on the given port", type=int)


class StatsHandler(tornado.web.RequestHandler):
    """
    URL: /api/stats/<daily|weekly|monthly>/<username>/
    """

    def get(self, interval, username):
        try:
            get_data_function = dict(INTERVALS)[interval]
            self.write(get_data_function(username))
        except KeyError:
            self.write(
                f"Could not find feed named '{interval}'.\
                Please try 'today', 'daily', 'weekly', or 'monthly.'")


def run_server():
    tornado.options.parse_command_line()
    app = tornado.wsgi.WSGIApplication([
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
    print("[LISTEN] http://localhost:8888")
    print("---")
    print("[DAILY] http://localhost:8888/api/stats/daily/droxey/")
    print("---")
    run_server()
