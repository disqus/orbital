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

    brew install geoip libevent
    pip install -r requirements.txt


Install Maxmind's GeoIP city data files to /usr/share/GeoIP/

::

    cp GeoIPCity.dat /usr/share/GeoIP/GeoIPCity.dat

Run the server

::

    python server.py

In another process, send sample data using ``feeder.py``

::

    python feeder.py

Configure haproxy (or something) to forward websockets on port 80 to 
port 7000, and setup something to serve site/.


Credits
=======

Map design and original concept from Mozilla's Glow project.