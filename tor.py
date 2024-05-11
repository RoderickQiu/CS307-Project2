from tornado.wsgi import *
from tornado.httpserver import *
from tornado.ioloop import *

from backend.app import app

s = HTTPServer(WSGIContainer(app))
s.bind(5000, "0.0.0.0")
s.start(1)
IOLoop.instance().start()
