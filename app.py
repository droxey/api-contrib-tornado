"""
server.py
Simple Tornado + Gevent API for GitHub contributions.
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

    def get(self, *args, **kwargs):
        try:
            interval_func = dict(INTERVALS)[args[0]]
            username = args[1]
            returned_data = interval_func(username)
            self.write(returned_data)
        except KeyError:
            self.write(
                f"Could not find feed for interval '{args[0]}'.\
                Please try 'daily', 'weekly' or 'monthly.'")


def run_server():
    app = tornado.wsgi.WSGIApplication([
        (r"/api/stats/(\w+)+/(\w+)+/$", StatsHandler),
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
