Orbital
=======

Orbital was built as an in-house demo for DISQUS to show a realtime representation of comments as
they happen on the network. It was heavily inspired by Mozilla's Glow project, but was mostly
rewritten in order to achieve true real-time. It was originally released to the public at PyCon
2012.

It's a simple demonstration of how easy you can achieve something like this with just
a little bit of Python and JavaScript code in modern browsers.

The code itself does not contain the firehose-like mechanism DISQUS uses to obtain the data from
their API. It does, however, contain a script which allows you to send mock data to demonstrate
how to create a publisher.

You can view the current version of orbital on the web at http://map.labs.disqus.com

.. image:: https://github.com/disqus/orbital/raw/master/example.png

Setup
=====

You can install most requirements via Homebrew and PIP

::

    brew install geoip libevent zeromq
    pip install -r requirements.txt


Install Maxmind's GeoIP city data files to /usr/share/GeoIP/

::

    cp GeoIPCity.dat /usr/share/GeoIP/GeoIPCity.dat

Run the server

::

    python server.py

Configure haproxy (or something) to forward websockets on port 80 to
port 7000, and setup something to serve site/.

Streaming Data
==============

Two example feeders are included. One explicitly takes your accounts DISQUS data and
feeds it in through the production DISQUS API. For example, if you run three forums,
it will continually stream data for all comments made on those forums through the
server. The other feeder will simply send fake data, and can be used as example code
to create your own custom data feeder.

Streaming DISQUS Data
---------------------

To stream data from DISQUS you'll first need to configure the application. To do this
visit the following URL, and register a new application::

    https://disqus.com/api/applications/register/

Once you've created the application, make sure the Default Access (under "Settings") is
set to "Read, Write, and Manage Forums". You'll need the Manage Forums bit explicitly,
as otherwise you wont gain admin access to the forums you moderate, which means DISQUS
won't send any private user data (such as IPs).

First you'll want to copy the default configuration file::

    cp app.cfg.example app.cfg

Now open this file in your favorite editor and adjust the settings to match your
API application. You'll specifically need the values for "Consumer Secret" and "Access Token".

Finally, run the feeder::

    python disqus_feeder.py

Streaming Example Data
----------------------

The second stream which is included sends sample data which is useful for modeling and testing your
frontend application. No configuration is required for this stream, and you can simply run it::

    python dummy_feeder.py

Credits
=======

Map design and original concept from Mozilla's Glow project.