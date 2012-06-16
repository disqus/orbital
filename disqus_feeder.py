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
import disqusapi
import os
import pygeoip
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

    # The path to your (non-free) GeoIP city data file
    # purchase this from http://www.maxmind.com/app/city
    'GEOIP_PATH': '/usr/share/GeoIP/GeoIPCity.dat',

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

# disqusapi does not provide first-class support for gevent (yet)
gevent.monkey.patch_all()

# load our default settings
load_settings('app.cfg', config, silent=False)


assert config['API_SECRET'], "You must set your API_SECRET!"
assert config['ACCESS_TOKEN'], "You must set your ACCESS_TOKEN!"


api = disqusapi.DisqusAPI(secret_key=config['API_SECRET'])
geocoder = pygeoip.GeoIP(config['GEOIP_PATH'], pygeoip.MEMORY_CACHE)


def geocode_addr(addr):
    try:
        return geocoder.record_by_addr(addr)
    except pygeoip.GeoIPError, e:
        log_exception(e)
        return {}


def anonymize(post, country_code):
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
        if 'ipAddress' not in post:
            print 'Post %r does not have ipAddress field' % post['id']
            return

        result = geocode_addr(post['ipAddress'])
        if not result:
            print 'Could not geocode post %r with ipAddress=%r' % (post['id'], post['ipAddress'])
            return

        print "New post", post['id']

        if result['metro_code']:
            loc = result['metro_code']
        elif result['city']:
            loc = '%s, %s' % (result['city'].decode('latin1'), result['country_name'].decode('latin1'))
        else:
            loc = result['country_name']
        data = {
            'post': anonymize(post, result['country_code']),
            'loc': loc,
            'lat': result['latitude'],
            'lng': result['longitude'],
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
