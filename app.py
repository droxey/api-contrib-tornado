"""
server.py
Simple Tornado + Gevent API for GitHub contributions.
"""
from tornado.web import RequestHandler
from tornado.wsgi import WSGIApplication
from gevent.pywsgi import WSGIServer
from contributions import get_contributions_daily, \
    get_contributions_weekly, get_contributions_monthly


INTERVALS = (
    ('daily', get_contributions_daily),
    ('weekly', get_contributions_weekly),
    ('monthly', get_contributions_monthly)
)


class StatsHandler(RequestHandler):
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


if __name__ == "__main__":
    print("[LISTEN] http://localhost:8888")
    print("---")
    print("[DAILY] http://localhost:8888/api/stats/daily/droxey/")
    print("---")
    APP = WSGIApplication([
        (r"/api/stats/(\w+)+/(\w+)+/$", StatsHandler),
    ], **{})
    SERVER = WSGIServer(('', 8888), APP)
    SERVER.serve_forever()
