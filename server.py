"""
orbital server
~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import json
import gevent
import mimetypes
import os.path

from multiprocessing import Process
from gevent import pywsgi, monkey
from geventwebsocket.handler import WebSocketHandler

from gevent_zeromq import zmq

monkey.patch_all()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'site'))


def run_publisher():
    """
    Pulls data from postevent and publishes to local subscribers
    """
    context = zmq.Context()

    publisher = context.socket(zmq.PUB)
    publisher.bind('tcp://127.0.0.1:5555')

    server = context.socket(zmq.PULL)
    server.bind('tcp://127.0.0.1:5556')

    while True:
        message = server.recv()

        publisher.send(message)
        gevent.sleep(0.1)

    publisher.close()


def run_websockets():
    def handle_ws(ws, environ):
        context = zmq.Context()

        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://127.0.0.1:5555")
        subscriber.setsockopt(zmq.SUBSCRIBE, "")

        print "[%s] Client connected" % environ['REMOTE_ADDR']

        params = None

        try:
            while True:
                if params is None:
                    print '[%s] Waiting on subscription params' % environ['REMOTE_ADDR']
                    m = ws.receive()
                    if not m:
                        return
                    cmd, args = m.split(' ', 1)
                    args = args.strip()
                    if args == '':
                        args = '*'

                    if cmd != 'SUB':
                        return

                    if args == '*':
                        params = {}
                    else:
                        params = dict(a.split('=') for a in args.split('&'))

                        for key, value in params.iteritems():
                            params[key] = map(lambda x: x.strip().lower(), value.split(' OR '))

                    print "[%s] Subscription established %s" % (environ['REMOTE_ADDR'], params)

                message = subscriber.recv()

                try:
                    data = json.loads(message)['post']
                except KeyError:
                    print 'Invalid data', message
                    continue

                if 'forum' in params and data['forum_id'] not in params['forum']:
                    continue

                if 'query' in params and data['thread_title'] not in params['query']:
                    continue

                ws.send(message)
        finally:
            subscriber.close()
            print "[%s] Client disconnected" % environ['REMOTE_ADDR']

    def handle(environ, start_response):
        path_info = environ['PATH_INFO']
        if path_info.endswith('/'):
            path_info += 'index.html'
        path = os.path.abspath(os.path.join(ROOT, path_info[1:]))

        if not path.startswith(ROOT) or not os.path.exists(path):
            start_response("404 Not Found", [])
            return []

        content_type = mimetypes.guess_type(path)[0]

        start_response("200 OK", [('Content-Type', content_type)])
        return [open(path, 'r').read()]

    def app(environ, start_response):
        if environ['PATH_INFO'] == '/' and 'wsgi.websocket' in environ:
            return handle_ws(environ['wsgi.websocket'], environ)
        return handle(environ, start_response)

    context = zmq.Context()

    server = context.socket(zmq.PULL)
    server.connect('tcp://127.0.0.1:5556')

    server = pywsgi.WSGIServer(('0.0.0.0', 7000), app,
        handler_class=WebSocketHandler)

    server.serve_forever()


def main():
    procs = [
        Process(target=run_publisher),
        Process(target=run_websockets),
    ]

    for p in procs:
        p.start()

if __name__ == "__main__":
    main()
