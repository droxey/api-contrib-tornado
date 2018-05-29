"""
server.py
Simple Tornado API for GitHub contributions.
"""
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.autoreload
import tornado.wsgi

from contributions import get_contributions_daily, \
    get_contributions_weekly, get_contributions_monthly, \
    get_contributions_today


INTERVALS = (
    ('today', get_contributions_today),
    ('daily', get_contributions_daily),
    ('weekly', get_contributions_weekly),
    ('monthly', get_contributions_monthly)
)


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
    app = tornado.wsgi.WSGIApplication([
        (r"/api/stats/([daily|weekly|monthly|today]+)/(\w+)+/$", StatsHandler),
    ], **{
        'debug': True,
    })
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(app)
    )
    http_server.listen(8888)
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
