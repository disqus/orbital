#!/usr/bin/env python
"""
orbital disqus data feeder
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import gevent
import gevent.queue
import gevent.monkey

# disqusapi does not provide first-class support for gevent (yet)
gevent.monkey.patch_all()

import disqusapi
import os
import traceback

from gevent_zeromq import zmq

try:
    from raven.base import Client
    raven = Client(os.environ['SENTRY_DSN'])
except:
    raven = None

# Create app.cfg and specify the following globals within it
config = {
    # Your DISQUS API Secret key
    # find this at https://disqus.com/api/applications/
    'API_SECRET': '',

    # Your DISQUS API Access Token
    # find this at https://disqus.com/api/applications/
    'ACCESS_TOKEN': '',

    # The zeromq socket for the Orbital publisher server
    'SERVER': 'tcp://127.0.0.1:5556',
}


def load_settings(filename, config, silent=True):
    import errno
    import imp

    mod = imp.new_module('config')
    mod.__file__ = filename
    try:
        execfile(filename, mod.__dict__)
    except IOError, e:
        if silent and e.errno in (errno.ENOENT, errno.EISDIR):
            return False
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise

    for x in dir(mod):
        if x.upper() == x:
            config[x] = getattr(mod, x)


def log_exception(e):
    if raven:
        raven.captureException()
    traceback.print_exc()

# load our default settings
load_settings('app.cfg', config, silent=False)


assert config['API_SECRET'], "You must set your API_SECRET!"
assert config['ACCESS_TOKEN'], "You must set your ACCESS_TOKEN!"


api = disqusapi.DisqusAPI(secret_key=config['API_SECRET'])


def anonymize(post):
    return {
        'link': post['thread']['link'],
        'title': post['thread']['title'],
        'icon': 'http://disqus.com/api/forums/favicons/%s.jpg' % (post['forum'],)
    }


def main():
    queue = gevent.queue.Queue(1000)
    context = zmq.Context()
    pub = context.socket(zmq.PUSH)
    pub.connect(config['SERVER'])

    def handle_post(post):
        if not post.get('approxLoc'):
            print 'Post %r does not have approxLoc field' % post['id']
            return

        print "New post", post['id']

        data = {
            'post': anonymize(post),
            'lat': post['approxLoc']['lat'],
            'lng': post['approxLoc']['lng'],
        }
        try:
            queue.put_nowait(data)
        except gevent.queue.Full:
            return

    def run_poller():
        cursor = ''
        order = 'desc'
        while True:
            print 'Fetching new posts (cursor is %r)' % cursor
            try:
                response = api.posts.list(cursor=cursor, forum=":moderated", order=order, related=['thread'],
                    limit=100, access_token=config['ACCESS_TOKEN'])
            except (SystemExit, KeyboardInterrupt):
                raise
            except Exception, e:
                log_exception(e)
                gevent.sleep(.3)
                continue

            cursor = response.cursor['next']
            order = 'asc'

            for post in response:
                try:
                    handle_post(post)
                except (SystemExit, KeyboardInterrupt):
                    raise
                except Exception, e:
                    log_exception(e)
                    continue
                gevent.sleep(0)

            gevent.sleep(.2)

    def run_feeder():
        while True:
            data = queue.get()
            pub.send_json(data)
            gevent.sleep(0.2)

    procs = [
        gevent.spawn(run_poller),
        gevent.spawn(run_feeder),
    ]

    for proc in procs:
        proc.join()

if __name__ == '__main__':
    main()
