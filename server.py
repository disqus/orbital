"""
orbital server
~~~~~~~~~~~~~~

The server consists of two subprocesses, and several greenlets.

The first process runs the actual web server (which includes a websocket
server). It does this via two greenlets, one which handles the actual web
requests, and the other which handles publishing messages to the websocket
client.

The second process runs the zeromq subscriber, which listens for messages
and republishes them to all websocket server clients.

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import json
import gevent
import mimetypes
import os.path
import uuid

from gevent import pywsgi, monkey
from gevent_zeromq import zmq
from geventwebsocket.handler import WebSocketHandler
from urlparse import urlparse

monkey.patch_all()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'site'))


class WebsocketPublisher(object):
    """
    Represents the websocket publisher, which receives messages
    from the feeder, and sends them to the websocket client.

    It's important that this is in a separate greenlet from the receive
    call as we'll block otherwise, and either not be able to send messages
    or not being able to receive future commands.
    """
    def __init__(self, subscriber, ws, params=None):
        self.subscriber = subscriber
        self.ws = ws
        self.params = params

    def run(self):
        ws = self.ws
        subscriber = self.subscriber
        while True:
            params = self.params

            message = subscriber.recv()

            if params is None:
                continue

            try:
                data = json.loads(message)['post']
            except KeyError:
                print 'Invalid data', message
                continue

            if params.get('domain'):
                if not data.get('link'):
                    continue

                domain = urlparse(data['link']).hostname.split('.')
                if not any(domain[-len(d):] == d for d in params['domain']):
                    continue

            if params.get('query') and not any(t in data['title'].lower() for t in params['query']):
                continue

            ws.send(message)


def run_publisher():
    """
    Pulls data from postevent and publishes to local subscribers
    """
    print "Publisher running, waiting for data.."

    context = zmq.Context()

    publisher = context.socket(zmq.PUB)
    publisher.bind('tcp://127.0.0.1:5555')

    server = context.socket(zmq.PULL)
    server.bind('tcp://127.0.0.1:5556')

    while True:
        message = server.recv()

        publisher.send(message)

    publisher.close()


def run_websockets():
    """
    Runs the websocket server (which also handles normal HTTP connections for serving
    the static assets).
    """
    clients = set()

    def handle_ws(ws, environ):
        context = zmq.Context()

        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://127.0.0.1:5555")
        subscriber.setsockopt(zmq.SUBSCRIBE, "")

        client_id = uuid.uuid4().hex
        clients.add(client_id)
        publisher = WebsocketPublisher(subscriber, ws)
        publisher_thread = gevent.spawn(publisher.run)

        print "[%s] Client connected %r (%s clients total)" % (client_id, environ['REMOTE_ADDR'], len(clients), )

        try:
            while True:
                message = ws.receive()
                if not message:
                    return

                message_bits = message.split(' ', 1)

                cmd = message_bits[0]

                if cmd == 'OK':
                    continue

                if cmd == 'SUB':
                    if len(message_bits) == 2:
                        args = message_bits[-1]
                    else:
                        args = ''

                    args = args.strip()
                    if args == '':
                        args = '*'

                    if args == '*':
                        params = {}
                    else:
                        params = dict(a.split('=') for a in args.split('&'))

                        for key, value in params.iteritems():
                            params[key] = filter(bool, map(lambda x: x.strip().lower(), value.split(' OR ')))

                            if key == 'domain':
                                params[key] = [d.split('.') for d in params[key]]

                    publisher.params = params

                    print "[%s] Subscription established %s" % (client_id, params)

        finally:
            publisher_thread.kill()
            subscriber.close()

            clients.remove(client_id)

            print "[%s] Client disconnected" % client_id

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

    host = '0.0.0.0'
    port = 7000

    print "Listening for connections on %s:%s" % (host, port)

    server = pywsgi.WSGIServer((host, port), app,
        handler_class=WebSocketHandler)

    server.serve_forever()


def main():
    procs = [
        gevent.spawn(run_publisher),
        gevent.spawn(run_websockets),
    ]

    for p in procs:
        p.join()

if __name__ == "__main__":
    main()
