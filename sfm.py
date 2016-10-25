#!/usr/bin/env python
# coding: utf8


import logging
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.netutil
from settings import *
from handler import *


def init_log():
    logging.basicConfig(format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                        datefmt='%m-%d %H:%M:%S', level=logging.DEBUG)
    #定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s'))
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)





class Application(tornado.web.Application):

    def __init__(self):
        url_patterns = [
            (r'/api/order/.*', OrderHandler),
            (r'/api/user/.*', UserHandler),
            (r'/api/cart/.*', CartHandler),
            (r'/api/webhooks/.*', WebhookHandler),
        ]
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": CONFIG['DEBUG']
        }
        super(Application, self).__init__(url_patterns, debug=CONFIG['DEBUG'], **settings)



app = Application()

if __name__ == '__main__':
    init_log()

    """
     By default, a blocking implementation is used (which simply calls
    `socket.getaddrinfo`).  An alternative implementation can be
    chosen with the `Resolver.configure <.Configurable.configure>`
    class method::
    优化域名解析阻塞
    """
    tornado.netutil.Resolver.configure("tornado.netutil.ThreadedResolver")

    port = CONFIG['HTTP']['PORT']
    host = CONFIG['HTTP']['HOST']
    sockets = tornado.netutil.bind_sockets(port=port, address=host)
    logging.info('start server ip=%s, port=%s' %(host, port))
    tornado.process.fork_processes(0)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets=sockets)
    tornado.ioloop.IOLoop.current().start()