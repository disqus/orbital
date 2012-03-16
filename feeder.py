#!/usr/bin/env python
"""
orbital feeder
~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import gevent
from gevent import monkey
import pygeoip
import random

from gevent_zeromq import zmq

monkey.patch_all()

GEOIP_PATH = '/usr/share/GeoIP/GeoIPCity.dat'
SERVER = 'tcp://0.0.0.0:5556'

# list of country codes that should be anonymized
COUNTRY_BLACKLIST = set([
    'IR',
    'SA',
    'DE',
])

geocoder = pygeoip.GeoIP(GEOIP_PATH, pygeoip.MEMORY_CACHE)


def geocode_addr(addr):
    return geocoder.record_by_addr(addr)


def generate_ip():
    return '%s.%s.%s.%s' % (random.randint(1, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def anonymize(post, country_code):
    result = {
        'thread_title': post['thread']['title'],
        'forum_id': post['forum'],
        # 'author_name': post['author']['name'],
        # 'avatar_url': post['author']['avatar']['cache'],
    }
    # if country_code in COUNTRY_BLACKLIST:
    #     result['avatar_url'] = 'http://mediacdn.disqus.com/1331069161/images/noavatar32.png'
    #     result['author_name'] = 'Anonymous'
    return result


messages = [
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "cnn",
      "parent": None,
      "author": {
        "username": "cnn-28a090ccdb81e5c31195d09ddd",
        "about": "",
        "remote": {
          "domain": "cnn",
          "identifier": "28a090ccdb81e5c31195d09ddd"
        },
        "name": "MartyGRMI",
        "url": "#",
        "id": "1431392",
        "profileUrl": "http://disqus.com/cnn-28a090ccdb81e5c31195d09ddd/",
        "emailHash": "56cc3e6d9ad85681c7fb6b1dd2132e8a",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/cnn-28a090ccdb81e5c31195d09ddd.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
      },
      "url": "http://www.cnn.com/2011/POLITICS/03/01/pol.budget.vote/index.html#comment-158476713",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476713",
      "thread": {
        "category": "207577",
        "reactions": 0,
        "identifiers": [
          "/2011/POLITICS/03/01/pol.budget.vote/index.html",
          "/2011/POLITICS/03%2"
        ],
        "forum": "cnn",
        "title": "House set to pass short-term government funding bill",
        "dislikes": 0,
        "isDeleted": False,
        "author": "335648",
        "userScore": 0,
        "id": "242913021",
        "isClosed": False,
        "posts": 177,
        "link": "http://www.cnn.com/2011/POLITICS/03/01/pol.budget.vote/index.html",
        "likes": 0,
        "message": "",
        "slug": "house_set_to_pass_short_term_government_funding_bill",
        "createdAt": "2011-03-01T17:05:37"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:52",
      "message": "\"The last Democratic Congress went on a spending spree\" - Was he talking about the tax break extension?  News flash.  Both parties have been on a spending spree for the last 40 years.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "godspolitics",
      "parent": 158451381,
      "author": {
        "username": "duhsciple",
        "about": "",
        "name": "duhsciple",
        "url": "",
        "profileUrl": "http://disqus.com/duhsciple/",
        "emailHash": "cf934a9d8411cf3cf2071a80707aa274",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/duhsciple.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/10/4134/avatar92.jpg?1281549413"
        },
        "isAnonymous": False,
        "id": "104134"
      },
      "url": "http://blog.sojo.net/2011/03/01/farewell-rob-bell-or-john-pipers-inferno/#comment-158476712",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476712",
      "thread": {
        "category": "38829",
        "reactions": 0,
        "identifiers": [
          "27053 http://blog.sojo.net/?p=27053"
        ],
        "forum": "godspolitics",
        "title": "&#8216;Farewell Rob Bell&#8217; (Or, John Piper&#8217;s Inferno)",
        "dislikes": 0,
        "isDeleted": False,
        "author": "94596",
        "userScore": 0,
        "id": "242969788",
        "isClosed": False,
        "posts": 23,
        "link": "http://blog.sojo.net/2011/03/01/farewell-rob-bell-or-john-pipers-inferno/",
        "likes": 1,
        "message": "Farewell Rob Bell. <a href=\"http://dsr.gd/fZqmd8\" rel=\"nofollow\">http://dsr.gd/fZqmd8</a>.With this three word tweet, John Piper, senior pastor at Bethlehem Baptist church in Minneapolis, Minnesota and elder statesman of the neo-reform stream of American Christianity, triggere",
        "slug": "8216farewell_rob_bell8217_or_john_piper8217s_inferno",
        "createdAt": "2011-03-01T18:14:52"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:52",
      "message": "When we draw lines for the purpose of exiling others, as the scribes and Pharisees did, just remember, Jesus is always on the other side of the line.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "sacbee",
      "parent": None,
      "author": {
        "username": "mcclatchy-2d0ccb71151ebf2f977e29b0c8a53e0a",
        "about": "",
        "remote": {
          "domain": "mcclatchy",
          "identifier": "9553d059edab4ebc45f6796e86231676-881129"
        },
        "name": "machkarl",
        "url": "",
        "id": "5752799",
        "profileUrl": "http://disqus.com/mcclatchy-2d0ccb71151ebf2f977e29b0c8a53e0a/",
        "emailHash": "7b09a0b77ca9408899b70ed13d857b2a",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/mcclatchy-2d0ccb71151ebf2f977e29b0c8a53e0a.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
      },
      "url": "http://www.sacbee.com/2011/03/01/3438590/uc-davis-may-ax-500-jobs-to-cope.html#comment-158476708",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476708",
      "thread": {
        "category": "409047",
        "reactions": 0,
        "identifiers": [
          "3438590"
        ],
        "forum": "sacbee",
        "title": "UC Davis may ax 500 jobs to cope with budget cuts",
        "dislikes": 0,
        "isDeleted": False,
        "author": "2918496",
        "userScore": 0,
        "id": "242559960",
        "isClosed": False,
        "posts": 109,
        "link": "http://www.sacbee.com/2011/03/01/3438590/uc-davis-may-ax-500-jobs-to-cope.html",
        "likes": 1,
        "message": "",
        "slug": "uc_davis_may_ax_500_jobs_to_cope_with_budget_cuts",
        "createdAt": "2011-03-01T08:04:05"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:52",
      "message": "If they actually stopped the unnecessary pey increases and had they employees pay more of their benefits and medical care, ie. sharing the pain, they would have to lay off far fewer and if they get rid of the diversity departments they would need no layoffs!",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "vanguardngr",
      "parent": 158440408,
      "author": {
        "username": "DanielOsazuwa",
        "about": "",
        "name": "DanielOsazuwa",
        "url": "",
        "profileUrl": "http://disqus.com/DanielOsazuwa/",
        "emailHash": "683a79486132fe3b36757b9c385fec59",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/DanielOsazuwa.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/550/509/avatar92.jpg?1290406620"
        },
        "isAnonymous": False,
        "id": "5500509"
      },
      "url": "http://www.vanguardngr.com/2011/03/police-arrest-cleric-4-others-for-defacing-jonathans-posters/#comment-158476711",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476711",
      "thread": {
        "category": "507293",
        "reactions": 0,
        "identifiers": [],
        "forum": "vanguardngr",
        "title": "Police arrest cleric, 4 others for defacing Jonathan's posters - Vanguard (Nigeria)",
        "dislikes": 0,
        "isDeleted": False,
        "author": "4841126",
        "userScore": 0,
        "id": "243018089",
        "isClosed": False,
        "posts": 25,
        "link": "http://www.vanguardngr.com/2011/03/police-arrest-cleric-4-others-for-defacing-jonathans-posters/",
        "likes": 0,
        "message": "",
        "slug": "police_arrest_cleric_4_others_for_defacing_jonathans_posters_vanguard_nigeria",
        "createdAt": "2011-03-01T19:11:19"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:52",
      "message": "THAT IS IF HIS LORDSHIP, ASIWAJU BOLA AHMED TINUBU WILL ALLOW THE WISHES OF NIGERIANS TO PREVAIL. <br><br>WITHOUT THE ALLIANCE BETWEEN CPC AND ACN, PDP WILL WIN.<br><br>NIGERIANS, HOLD TINUBU RESPONSIBLE IF PDP RIG THEMSELVES  BACK TO POWER.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "foxnews",
      "parent": 158475408,
      "author": {
        "username": "fox-news-9b0171aefc9ca5a885d9fa1386014482",
        "about": "",
        "remote": {
          "domain": "fox-news",
          "identifier": "jgrover"
        },
        "name": "jgrover",
        "url": "",
        "id": "5508602",
        "profileUrl": "http://disqus.com/fox-news-9b0171aefc9ca5a885d9fa1386014482/",
        "emailHash": "d359745f0d2143ca1a08e81c729cc49d",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/fox-news-9b0171aefc9ca5a885d9fa1386014482.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
      },
      "url": "http://www.foxnews.com/politics/2011/03/01/government-waste-numbers-report-identifies-dozens-duplicative-programs/#comment-158476707",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476707",
      "thread": {
        "category": "462854",
        "reactions": 0,
        "identifiers": [
          "7431d2323e17e210VgnVCM10000086c1a8c0RCRD",
          "7431d2323e17e210Vg",
          "7431d232",
          "7431d2323e17e21"
        ],
        "forum": "foxnews",
        "title": "Government Waste By the Numbers: Report Identifies Dozens of Overlapping Programs",
        "dislikes": 0,
        "isDeleted": False,
        "author": "2500343",
        "userScore": 0,
        "id": "242829377",
        "isClosed": False,
        "posts": 1680,
        "link": "http://www.foxnews.com/politics/2011/03/01/government-waste-numbers-report-identifies-dozens-duplicative-programs/",
        "likes": 0,
        "message": "",
        "slug": "government_waste_by_the_numbers_report_identifies_dozens_of_duplicative_programs",
        "createdAt": "2011-03-01T15:23:28"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:51",
      "message": "love it.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "milenio",
      "parent": 158441356,
      "author": {
        "username": "RosiTaFrescA",
        "about": "",
        "name": "Jaime Costecho",
        "url": "",
        "profileUrl": "http://disqus.com/RosiTaFrescA/",
        "emailHash": "fc27bf2dae6c049d9403e0e2226b546f",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/RosiTaFrescA.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/546/8123/avatar92.jpg?1299016585"
        },
        "isAnonymous": False,
        "id": "5468123"
      },
      "url": "http://www.milenio.com/node/659095#comment-158476706",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476706",
      "thread": {
        "category": "219102",
        "reactions": 0,
        "identifiers": [],
        "forum": "milenio",
        "title": "Anuncia CNTE nuevas manifestaciones en capital michoacana ",
        "dislikes": 0,
        "isDeleted": False,
        "author": "851487",
        "userScore": 0,
        "id": "243086235",
        "isClosed": False,
        "posts": 3,
        "link": "http://www.milenio.com/node/659095",
        "likes": 0,
        "message": "",
        "slug": "anuncia_cnte_nuevas_manifestaciones_en_capital_michoacana",
        "createdAt": "2011-03-01T20:47:19"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:51",
      "message": "deja de decir  tonterias!! el CNTe nos pone un ejemplo a todos! valor",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "fotbollskanalensehyllman",
      "parent": 158472307,
      "author": {
        "username": "Oooo_to_be_aGooner",
        "about": "",
        "name": "OtbaG",
        "url": "",
        "profileUrl": "http://disqus.com/Oooo_to_be_aGooner/",
        "emailHash": "46da161bb9c68f71b8dc6cf743339e9a",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/Oooo_to_be_aGooner.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/230/3592/avatar92.jpg?1282666536"
        },
        "isAnonymous": False,
        "id": "2303592"
      },
      "url": "http://hyllman.fotbollskanalen.se/2011/03/01/head-cases/#comment-158476705",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476705",
      "thread": {
        "category": "456844",
        "reactions": 0,
        "identifiers": [
          "919 http://hyllman.wordpress-mu.tv4.se/?p=919"
        ],
        "forum": "fotbollskanalensehyllman",
        "title": "Head Cases",
        "dislikes": 0,
        "isDeleted": False,
        "author": "614797",
        "userScore": 0,
        "id": "242634531",
        "isClosed": False,
        "posts": 456,
        "link": "http://hyllman.fotbollskanalen.se/2011/03/01/head-cases/",
        "likes": 3,
        "message": "We judge ourselves on the pride we create for our fanbase. That pride is created through all kinds of different things. One of them clearly is trophies. That is critical for a club of Arsenal's size but there are other things that drive pride, including the style of football we",
        "slug": "head_cases",
        "createdAt": "2011-03-01T09:56:54"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:51",
      "message": "Typiskt toppmatch. United dominerar frsta, Chelsea andra. 1-1 rttvist men det brukar ju oftast avgras av misstag, magi eller missar frn domaren.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "cnn",
      "parent": 158469065,
      "author": {
        "username": "cnn-131202562d88379dddcd1c60ee",
        "about": "",
        "remote": {
          "domain": "cnn",
          "identifier": "131202562d88379dddcd1c60ee"
        },
        "name": "sawyer",
        "url": "#",
        "id": "2177515",
        "profileUrl": "http://disqus.com/cnn-131202562d88379dddcd1c60ee/",
        "emailHash": "68c13b61aa22eb72ed4bca59627c4407",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/cnn-131202562d88379dddcd1c60ee.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
      },
      "url": "http://www.cnn.com/2011/CRIME/03/01/us.gang.arrests/index.html#comment-158476704",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476704",
      "thread": {
        "category": "207582",
        "reactions": 0,
        "identifiers": [
          "/2011/CRIME/03/01/us.gang.arrests/index.html"
        ],
        "forum": "cnn",
        "title": "Drug gang sweep results in hundreds of arrests",
        "dislikes": 0,
        "isDeleted": False,
        "author": "335648",
        "userScore": 0,
        "id": "243016616",
        "isClosed": False,
        "posts": 191,
        "link": "http://www.cnn.com/2011/CRIME/03/01/us.gang.arrests/index.html",
        "likes": 0,
        "message": "",
        "slug": "drug_gang_sweep_results_in_hundreds_of_arrests",
        "createdAt": "2011-03-01T19:09:22"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:51",
      "message": "Then we the tax payer will have to pay for all the addiction centers to bail out jobless dead beat drug addicts.  Or maybe you can help them all on you income...you moron!",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "pequenademais",
      "parent": None,
      "author": {
        "name": "Paula",
        "url": "",
        "profileUrl": "http://disqus.com/guest/f9fe0b8b297df1f5fa1e9ec508ba931e/",
        "emailHash": "f9fe0b8b297df1f5fa1e9ec508ba931e",
        "avatar": {
          "permalink": "http://www.gravatar.com/avatar.php?gravatar_id=f9fe0b8b297df1f5fa1e9ec508ba931e&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png",
          "cache": "http://www.gravatar.com/avatar.php?gravatar_id=f9fe0b8b297df1f5fa1e9ec508ba931e&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png"
        },
        "isAnonymous": True,
      },
      "url": "http://pequenademais.blogspot.com/2011/02/happy-or-sad-you-choose.html#comment-158476703",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476703",
      "thread": {
        "category": "58629",
        "reactions": 0,
        "identifiers": [],
        "forum": "pequenademais",
        "title": "happy or sad, you choose.",
        "dislikes": 0,
        "isDeleted": False,
        "author": "143736",
        "userScore": 0,
        "id": "227410240",
        "isClosed": False,
        "posts": 2,
        "link": "http://pequenademais.blogspot.com/2011/02/happy-or-sad-you-choose.html",
        "likes": 0,
        "message": "",
        "slug": "happy_or_sad_you_choose",
        "createdAt": "2011-02-10T23:22:26"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:50",
      "message": "s3 pra te lembrar que ainda vejo o seu blog...<br><br>bjokas!!",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "foxnews",
      "parent": 158476040,
      "author": {
        "username": "fox-news-fb3d3543a5e8b534f1a434dfbb609f29",
        "about": "",
        "remote": {
          "domain": "fox-news",
          "identifier": "clearedtoland"
        },
        "name": "clearedtoland",
        "url": "",
        "id": "7538023",
        "profileUrl": "http://disqus.com/fox-news-fb3d3543a5e8b534f1a434dfbb609f29/",
        "emailHash": "ce91b3d6da31c75d97afe84796a79623",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/fox-news-fb3d3543a5e8b534f1a434dfbb609f29.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
      },
      "url": "http://www.foxnews.com/scitech/2011/03/01/house-pursue-efforts-eliminate-funding-climate-group/#comment-158476699",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476699",
      "thread": {
        "category": "462855",
        "reactions": 0,
        "identifiers": [
          "4bb15d1ffce5e210VgnVCM10000086c1a8c0RCRD",
          "4bb15d1ffce5e210VgnVCM10000086c1a8c0R",
          "4bb15d1ffce5e210VgnVCM10000"
        ],
        "forum": "foxnews",
        "title": "House Will Pursue Efforts to Eliminate US Funding for UN Climate Group",
        "dislikes": 0,
        "isDeleted": False,
        "author": "2500343",
        "userScore": 0,
        "id": "242942864",
        "isClosed": False,
        "posts": 1954,
        "link": "http://www.foxnews.com/scitech/2011/03/01/house-pursue-efforts-eliminate-funding-climate-group/",
        "likes": 0,
        "message": "",
        "slug": "house_will_pursue_efforts_to_eliminate_us_funding_for_un_climate_group",
        "createdAt": "2011-03-01T17:43:15"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:50",
      "message": "Now that was quick. I appreciate it!",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "sheposts",
      "parent": 158392221,
      "author": {
        "name": "Candice",
        "url": "http://www.fashionablyorganized.com",
        "profileUrl": "http://disqus.com/guest/492029b91e40ec2570782be5b725263b/",
        "emailHash": "492029b91e40ec2570782be5b725263b",
        "avatar": {
          "permalink": "http://www.gravatar.com/avatar.php?gravatar_id=492029b91e40ec2570782be5b725263b&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png",
          "cache": "http://www.gravatar.com/avatar.php?gravatar_id=492029b91e40ec2570782be5b725263b&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png"
        },
        "isAnonymous": True,
      },
      "url": "http://www.sheposts.com/node/981#comment-158476702",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476702",
      "thread": {
        "category": "325816",
        "reactions": 0,
        "identifiers": [
          "node/981"
        ],
        "forum": "sheposts",
        "title": "Cecily Kellogg's Daughter Booted From Preschool Over Blog",
        "dislikes": 0,
        "isDeleted": False,
        "author": "2353720",
        "userScore": 0,
        "id": "242485063",
        "isClosed": False,
        "posts": 95,
        "link": "http://www.sheposts.com/node/981",
        "likes": 4,
        "message": "",
        "slug": "cecily_kelloggs_daughter_booted_from_preschool_over_blog",
        "createdAt": "2011-03-01T05:55:53"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:50",
      "message": "\"You seem not to fully absorbing the fact that you made bad decisions...\" <br><br>Bad decisions according to who? Who gets to be the one who says she made bad decisions? She decided to express herself, and maybe that's different then the way you express yourself, but that doesn't make it a bad decision.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "engadget2",
      "parent": None,
      "author": {
        "username": "facebook-1145565120",
        "about": "",
        "remote": {
          "domain": "facebook",
          "identifier": "1145565120"
        },
        "name": "Lorenzo Berkley",
        "url": "http://www.facebook.com/wtfLORENZOidfc",
        "id": "6309181",
        "profileUrl": "http://disqus.com/facebook-1145565120/",
        "emailHash": "d41d8cd98f00b204e9800998ecf8427e",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/facebook-1145565120.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/630/9181/avatar92.jpg?1281549413"
        },
        "isAnonymous": False,
      },
      "url": "http://www.engadget.com/2011/01/20/t-mobile-confirms-galaxy-s-with-4g-android-based-sidekick-4g-ar/#comment-158476697",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476697",
      "thread": {
        "category": "426475",
        "reactions": 0,
        "identifiers": [
          "19808563"
        ],
        "forum": "engadget2",
        "title": "T-Mobile confirms Galaxy S with 4G, Android-based Sidekick 4G are coming",
        "dislikes": 0,
        "isDeleted": False,
        "author": "3712026",
        "userScore": 0,
        "id": "212859275",
        "isClosed": False,
        "posts": 205,
        "link": "http://www.engadget.com/2011/01/20/t-mobile-confirms-galaxy-s-with-4g-android-based-sidekick-4g-ar/",
        "likes": 1,
        "message": "",
        "slug": "t_mobile_confirms_galaxy_s_with_4g_android_based_sidekick_4g_are_coming",
        "createdAt": "2011-01-20T15:56:34"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:50",
      "message": "yay Samsung's bringing back the phone with too many buttons and pairing it with the OS that needs absolutely none ...i wonder how this will work out......?",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "appadvice",
      "parent": 153795416,
      "author": {
        "name": "end of tenancy cleaning",
        "url": "http://www.cleaninghouselondon.co.uk/",
        "profileUrl": "http://disqus.com/guest/cded8a1473ae277a3fcb79c8ac839bec/",
        "emailHash": "cded8a1473ae277a3fcb79c8ac839bec",
        "avatar": {
          "permalink": "http://www.gravatar.com/avatar.php?gravatar_id=cded8a1473ae277a3fcb79c8ac839bec&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png",
          "cache": "http://www.gravatar.com/avatar.php?gravatar_id=cded8a1473ae277a3fcb79c8ac839bec&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png"
        },
        "isAnonymous": True,
      },
      "url": "http://appadvice.com/appnn/2010/03/appisode-86-apple-does-more-spring-cleaning-race-against-android-users-and-a-new-accessory-alley/#comment-158476698",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476698",
      "thread": {
        "category": "210602",
        "reactions": 0,
        "identifiers": [
          "50366 http://appadvice.com/appnn/?p=50366"
        ],
        "forum": "appadvice",
        "title": "Appisode 86: Apple Does More Spring Cleaning, Race Against Android Users, And A New Accessory Alley!",
        "dislikes": 0,
        "isDeleted": False,
        "author": "959541",
        "userScore": 0,
        "id": "236956568",
        "isClosed": False,
        "posts": 12,
        "link": "http://appadvice.com/appnn/2010/03/appisode-86-apple-does-more-spring-cleaning-race-against-android-users-and-a-new-accessory-alley/",
        "likes": 0,
        "message": "",
        "slug": "appisode_86_apple_does_more_spring_cleaning_race_against_android_users_and_a_new_accessory_alley",
        "createdAt": "2010-03-05T02:25:07"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:50",
      "message": "oh don't speak. I still can't learn how to work with it phhhh",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "ign-blogs",
      "parent": 158441336,
      "author": {
        "username": "ign-e6b9a25c00972985f2df71ac94697f7d",
        "about": "",
        "remote": {
          "domain": "ign",
          "identifier": "284637493"
        },
        "name": "generic-man",
        "url": "http://people.ign.com/generic-man",
        "id": "6574893",
        "profileUrl": "http://disqus.com/ign-e6b9a25c00972985f2df71ac94697f7d/",
        "emailHash": "47b397c7e9725f6cf02098ffc79901a0",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/ign-e6b9a25c00972985f2df71ac94697f7d.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/657/4893/avatar92.jpg?1281549413"
        },
        "isAnonymous": False,
      },
      "url": "http://www.ign.com/blogs/generic-man/2011/03/01/3ds-into-the-depths/#comment-158476696",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476696",
      "thread": {
        "category": "520912",
        "reactions": 0,
        "identifiers": [
          "4d6d359c3831c82f1b0000ac"
        ],
        "forum": "ign-blogs",
        "title": "3DS - Into the Depths",
        "dislikes": 0,
        "isDeleted": False,
        "author": "3103639",
        "userScore": 0,
        "id": "243086501",
        "isClosed": False,
        "posts": 11,
        "link": "http://www.ign.com/blogs/generic-man/2011/03/01/3ds-into-the-depths/",
        "likes": 0,
        "message": "",
        "slug": "3ds_into_the_depths",
        "createdAt": "2011-03-01T20:47:38"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:50",
      "message": "Nah I can wait the month or 2 before I start gathering new gen games. I still have old ones I need to wrap up.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "mamapediasweetdeals",
      "parent": 158474760,
      "author": {
        "username": "SweetDeals",
        "about": "",
        "name": "SweetDeals",
        "url": "",
        "profileUrl": "http://disqus.com/SweetDeals/",
        "emailHash": "2a6dbe14ee579374df85db177ad99c6c",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/SweetDeals.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
        "id": "5092403"
      },
      "url": "http://deals.mamapedia.com/deals/discussion/twin-sisters-productions#comment-158476694",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476694",
      "thread": {
        "category": "518863",
        "reactions": 0,
        "identifiers": [
          "_twin-sisters-productions"
        ],
        "forum": "mamapediasweetdeals",
        "title": "Discuss this Deal: $15 for $30 Worth of Kid's Educational Products From Twin Sisters Productions - Mamapedia Sweet Deals",
        "dislikes": 0,
        "isDeleted": False,
        "author": "5037545",
        "userScore": 0,
        "id": "242691918",
        "isClosed": False,
        "posts": 9,
        "link": "http://deals.mamapedia.com/deals/discussion/twin-sisters-productions",
        "likes": 0,
        "message": "",
        "slug": "discuss_this_deal_15_for_30_worth_of_kids_educational_products_from_twin_sisters_productions_mamaped",
        "createdAt": "2011-03-01T11:35:14"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:50",
      "message": "I'm checking on this right now for you.<br>",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "cnn",
      "parent": 158473230,
      "author": {
        "username": "cnn-c2b65573e602a8e1a995d8cc6f",
        "about": "",
        "remote": {
          "domain": "cnn",
          "identifier": "c2b65573e602a8e1a995d8cc6f"
        },
        "name": "goldhiemer",
        "url": "#",
        "id": "7444471",
        "profileUrl": "http://disqus.com/cnn-c2b65573e602a8e1a995d8cc6f/",
        "emailHash": "77fec515147eb262072b56068d06ee23",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/cnn-c2b65573e602a8e1a995d8cc6f.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
      },
      "url": "http://www.cnn.com/2011/POLITICS/03/01/wisconsin.budget/index.html#comment-158476693",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476693",
      "thread": {
        "category": "207577",
        "reactions": 0,
        "identifiers": [
          "/2011/POLITICS/03/01/wisconsin.budget/index.html"
        ],
        "forum": "cnn",
        "title": "Wisconsin Senate leader meets AWOL Democrats as protests continue",
        "dislikes": 0,
        "isDeleted": False,
        "author": "335648",
        "userScore": 0,
        "id": "242523459",
        "isClosed": False,
        "posts": 1974,
        "link": "http://www.cnn.com/2011/POLITICS/03/01/wisconsin.budget/index.html",
        "likes": 0,
        "message": "",
        "slug": "new_wisconsin_budget_due_as_state_tries_to_patch_old_one",
        "createdAt": "2011-03-01T07:06:06"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:49",
      "message": "People will not move their business out of state because they have to pay more to get their nails done.  They will move their business out of state if their business cannot prosper.  And please quit saying taxing something means you hate something...it is too simplistic and unTrue.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "thoughtcatalog",
      "parent": 157916946,
      "author": {
        "name": "DaddyO",
        "url": "",
        "profileUrl": "http://disqus.com/guest/bfe562c54809afa5e822a5f11a260b80/",
        "emailHash": "bfe562c54809afa5e822a5f11a260b80",
        "avatar": {
          "permalink": "http://www.gravatar.com/avatar.php?gravatar_id=bfe562c54809afa5e822a5f11a260b80&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png",
          "cache": "http://www.gravatar.com/avatar.php?gravatar_id=bfe562c54809afa5e822a5f11a260b80&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png"
        },
        "isAnonymous": True,
      },
      "url": "http://thoughtcatalog.com/2011/soccer-player-kicks-an-owl-when-its-down-during-match/#comment-158476692",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476692",
      "thread": {
        "category": "282363",
        "reactions": 0,
        "identifiers": [
          "32318 http://thoughtcatalog.com/?p=32318"
        ],
        "forum": "thoughtcatalog",
        "title": "Private: Soccer Player Kicks An Owl When It&#8217;s Down During Match",
        "dislikes": 0,
        "isDeleted": False,
        "author": "1755784",
        "userScore": 0,
        "id": "242219198",
        "isClosed": False,
        "posts": 14,
        "link": "http://thoughtcatalog.com/2011/soccer-player-kicks-an-owl-when-its-down-during-match/",
        "likes": 0,
        "message": "The Colombian soccer player, a defender for Deportivo Pereira, kicked an injured owl when it landed on the pitch during a match against Atletico Junior of Barranquilla. The owl, it turns out, is Atletico Junior's mascot, and was hurt when it flew onto the field",
        "slug": "private_soccer_player_kicks_an_owl_when_it8217s_down_during_match",
        "createdAt": "2011-02-28T21:29:11"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:49",
      "message": "the owl died :(<br>",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "disqus",
      "parent": 158239640,
      "author": {
        "name": "David Cramer",
        "url": "",
        "profileUrl": "http://disqus.com/guest/f5d4b1fe68ab021021802422537b0b76/",
        "emailHash": "f5d4b1fe68ab021021802422537b0b76",
        "avatar": {
          "permalink": "http://www.gravatar.com/avatar.php?gravatar_id=f5d4b1fe68ab021021802422537b0b76&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png",
          "cache": "http://www.gravatar.com/avatar.php?gravatar_id=f5d4b1fe68ab021021802422537b0b76&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png"
        },
        "isAnonymous": False,
        "username": "zeeg",
      },
      "url": "http://www.cnsnews.com/node/81877#comment-158476691",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476691",
      "thread": {
        "category": "535626",
        "reactions": 0,
        "identifiers": [
          "node/81877"
        ],
        "forum": "disqus",
        "title": "Clinton: Too Much Ethanol Could Lead to Food Riots",
        "dislikes": 1,
        "isDeleted": False,
        "author": "3147682",
        "userScore": 0,
        "id": "239501400",
        "isClosed": False,
        "posts": 45,
        "link": "http://www.cnsnews.com/node/81877",
        "likes": 4,
        "message": "",
        "slug": "clinton_too_much_ethanol_could_lead_to_food_riots",
        "createdAt": "2011-02-24T20:06:56"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:49",
      "message": "I expect you are correct about Pittsburgh versus Waterloo air quality, but why is that germane to this discussion? <br><br>If what you say is True about all the boat motors that melt down over ethanol, the engineers best get to work. There is no excuse for ethanol to harm an engine. <br><br>These boat/motor manufacturers do approve ethanol in their motors; Yamaha, Tracker, Kawasaki, Mercury, OMC (Johnson/Evinrude), Pleasurecraft and Tigershark (Arctco). Sounds a bit like your list.<br><br>Why ethanol in small engines should be an issue where you live, but a non issue in my buddy John L's`` small engine shop, is beyond me. I have owned dozens of chain saws of all sizes and made by various maufacturers. I worked them very hard professionaly, always burning ethanol, and none of them ever had the slightest problem with ethanol. In spite of thousands of hours of work, very few breakdowns were even remotly related to the inner combustion workings, fuel system or carburetors of the saws. <br><br>I rather suspect some folks are just using ethanol as a scape goat to blame for normal equipment breakdowns. All engines break down eventualy, even ones that have not run on ethanol.<br><br>Ethanol is the most tested fuel additive in our history, by far, and has been proven over and over to cause no harm. You continue to make wild and speculative statements about ethanol. In my observation all of these objections are based on annecdotal evidence by folks that have not one iota of proof of what they say, as they blame ethanol with no proof whatsoever. <br><br>All I have read from you is purely rumor and speculation and baseless hearsay. You have no proof whatsoever that ethanol is a problem.<br><br>I do not need higher octane in my 1992 LeBaron. It is the government that is mandating it. I suggest you discss the reason for that issue with them.<br><br>The clean burning aspect of ethanol, however, makes all engines run better and longer, including boat motors and all small engines. The fears you have are just old wives tales.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "bellinghamherald",
      "parent": None,
      "author": {
        "username": "facebook-100001775604280",
        "about": "",
        "remote": {
          "domain": "facebook",
          "identifier": "100001775604280"
        },
        "name": "Mc Lovebuddy",
        "url": "http://www.facebook.com/people/Mc-Lovebuddy/100001775604280",
        "id": "5859059",
        "profileUrl": "http://disqus.com/facebook-100001775604280/",
        "emailHash": "d41d8cd98f00b204e9800998ecf8427e",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/facebook-100001775604280.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/585/9059/avatar92.jpg?1281549413"
        },
        "isAnonymous": False,
      },
      "url": "http://www.bellinghamherald.com/2011/03/01/1892658/shop-site-jaros-designs-wwwetsycomshopjarosdesigns.html#comment-158476690",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476690",
      "thread": {
        "category": "409004",
        "reactions": 0,
        "identifiers": [
          "1892658"
        ],
        "forum": "bellinghamherald",
        "title": "Shop site: Jaros Designs (www.etsy.com/shop/JarosDesigns)",
        "dislikes": 0,
        "isDeleted": False,
        "author": "2918496",
        "userScore": 0,
        "id": "243098771",
        "isClosed": False,
        "posts": 1,
        "link": "http://www.bellinghamherald.com/2011/03/01/1892658/shop-site-jaros-designs-wwwetsycomshopjarosdesigns.html",
        "likes": 0,
        "message": "",
        "slug": "shop_site_jaros_designs_wwwetsycomshopjarosdesigns",
        "createdAt": "2011-03-01T21:04:50"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:49",
      "message": "love this shop. i've been eyeing some of the items for a while. :)",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "firstshowing",
      "parent": 157999467,
      "author": {
        "username": "Xerxexx",
        "about": "",
        "name": "Xerxexx",
        "url": "",
        "profileUrl": "http://disqus.com/Xerxexx/",
        "emailHash": "01e24748b04c4b05969d92b17ee0bd9d",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/Xerxexx.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/632/5198/avatar92.jpg?1294554255"
        },
        "isAnonymous": False,
        "id": "6325198"
      },
      "url": "http://www.firstshowing.net/2011/daniel-day-lewis-viggo-mortensen-wanted-for-superman-roles/#comment-158476689",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476689",
      "thread": {
        "category": "397007",
        "reactions": 0,
        "identifiers": [
          "99739 http://www.firstshowing.net/?p=99739"
        ],
        "forum": "firstshowing",
        "title": "Daniel Day-Lewis & Viggo Mortensen Wanted for 'Superman' Roles?",
        "dislikes": 0,
        "isDeleted": False,
        "author": "3364802",
        "userScore": 0,
        "id": "242103865",
        "isClosed": False,
        "posts": 17,
        "link": "http://www.firstshowing.net/2011/daniel-day-lewis-viggo-mortensen-wanted-for-superman-roles/",
        "likes": 0,
        "message": "",
        "slug": "daniel_day_lewis_viggo_mortensen_wanted_for_superman_roles",
        "createdAt": "2011-02-28T18:32:29"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:49",
      "message": "its Earth Shattering.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "themindchannel",
      "parent": None,
      "author": {
        "username": "twitter-169222638",
        "about": "",
        "remote": {
          "domain": "twitter",
          "identifier": "169222638"
        },
        "name": "Dan Twin",
        "url": "http://twitter.com/xthegunshow",
        "id": "7730897",
        "profileUrl": "http://disqus.com/twitter-169222638/",
        "emailHash": "d41d8cd98f00b204e9800998ecf8427e",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/twitter-169222638.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/773/897/avatar92.jpg?1281549413"
        },
        "isAnonymous": False,
      },
      "url": "http://www.mindch.com/2011/03/first-gameplay-screenshot-of.html#comment-158476687",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476687",
      "thread": {
        "category": "469587",
        "reactions": 1,
        "identifiers": [],
        "forum": "themindchannel",
        "title": "THE MIND CHANNEL: First Gameplay Screenshot of Battlefield 3",
        "dislikes": 0,
        "isDeleted": False,
        "author": "4194778",
        "userScore": 0,
        "id": "243067756",
        "isClosed": False,
        "posts": 1,
        "link": "http://www.mindch.com/2011/03/first-gameplay-screenshot-of.html",
        "likes": 0,
        "message": "",
        "slug": "the_mind_channel_first_gameplay_screenshot_of_battlefield_3",
        "createdAt": "2011-03-01T20:20:59"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:48",
      "message": "Jesus Christ slowpoke.jpg",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "nationfoxnews",
      "parent": 158475765,
      "author": {
        "username": "fox-news-59431c87dc4b2c98cce35b569abb4319",
        "about": "",
        "remote": {
          "domain": "fox-news",
          "identifier": "abort_christ"
        },
        "name": "abort_christ",
        "url": "",
        "id": "6236051",
        "profileUrl": "http://disqus.com/fox-news-59431c87dc4b2c98cce35b569abb4319/",
        "emailHash": "a844b5385d52fe2c187e211d55464671",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/fox-news-59431c87dc4b2c98cce35b569abb4319.jpg",
          "cache": "http://mediacdn.disqus.com/1298421702/images/noavatar92.png"
        },
        "isAnonymous": False,
      },
      "url": "http://nation.foxnews.com/sarah-palin/2011/03/01/palin-appalled-obama-s-marriage-flip-flop#comment-158476686",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476686",
      "thread": {
        "category": "504118",
        "reactions": 0,
        "identifiers": [],
        "forum": "nationfoxnews",
        "title": "Palin 'Appalled' by Obama's Marriage Flip-Flop - Sarah Palin - Fox Nation",
        "dislikes": 0,
        "isDeleted": False,
        "author": "2500343",
        "userScore": 0,
        "id": "243065821",
        "isClosed": False,
        "posts": 141,
        "link": "http://nation.foxnews.com/sarah-palin/2011/03/01/palin-appalled-obama-s-marriage-flip-flop",
        "likes": 0,
        "message": "",
        "slug": "palin_appalled_by_obamas_marriage_flip_flop_sarah_palin_fox_nation",
        "createdAt": "2011-03-01T20:18:56"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:48",
      "message": "Doing quite well.  Won the 2008 Presidential election as a matter of fact!",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "telegraphuk",
      "parent": 158337065,
      "author": {
        "username": "HenkM",
        "about": "",
        "name": "HenkM",
        "url": "",
        "profileUrl": "http://disqus.com/HenkM/",
        "emailHash": "a700930c7ac24b9cbebdd0e268990049",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/HenkM.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/161/8601/avatar92.jpg?1264028568"
        },
        "isAnonymous": False,
        "id": "1618601"
      },
      "url": "http://www.telegraph.co.uk/news/newstopics/religion/8353496/Foster-parent-ban-no-place-in-the-law-for-Christianity-High-Court-rules.html#comment-158476685",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476685",
      "thread": {
        "category": "244200",
        "reactions": 191,
        "identifiers": [
          "8353496"
        ],
        "forum": "telegraphuk",
        "title": "Foster parent ban: 'no place&rsquo; in the law for Christianity, High Court rules",
        "dislikes": 0,
        "isDeleted": False,
        "author": "1343193",
        "userScore": 0,
        "id": "242298969",
        "isClosed": False,
        "posts": 1594,
        "link": "http://www.telegraph.co.uk/news/newstopics/religion/8353496/Foster-parent-ban-no-place-in-the-law-for-Christianity-High-Court-rules.html",
        "likes": 0,
        "message": "",
        "slug": "foster_parent_ban_no_placersquo_in_the_law_for_christianity_high_court_rules",
        "createdAt": "2011-02-28T23:36:32"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:48",
      "message": "How about Gay/Red Indians/ Indians/Muslims/Polyamoric/Wiccan/non believers/free thinkers/ Blond people/ Green eyed people/ not to forget handicapped people requesting the Queen to defend their equal rights on equal footing?",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "gazetaesportivanet",
      "parent": None,
      "author": {
        "name": "Gianpaolo",
        "url": "",
        "profileUrl": "http://disqus.com/guest/e227b42ce8e1ff1d08fe4db6cdceb38e/",
        "emailHash": "e227b42ce8e1ff1d08fe4db6cdceb38e",
        "avatar": {
          "permalink": "http://www.gravatar.com/avatar.php?gravatar_id=e227b42ce8e1ff1d08fe4db6cdceb38e&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png",
          "cache": "http://www.gravatar.com/avatar.php?gravatar_id=e227b42ce8e1ff1d08fe4db6cdceb38e&size=32&default=http://mediacdn.disqus.com/1298421702/images/noavatar32.png"
        },
        "isAnonymous": True,
      },
      "url": "http://www.gazetaesportiva.net/noticia/2011/03/palmeiras/empresario-negocia-com-o-galo-para-trazer-ricardo-bueno-ao-verdao.html#comment-158476688",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476688",
      "thread": {
        "category": "528502",
        "reactions": 6,
        "identifiers": [
          "nt-677332"
        ],
        "forum": "gazetaesportivanet",
        "title": "Emprese1rio negocia com o Galo para trazer Ricardo Bueno ao Verdo | Gazeta Esportiva.Net",
        "dislikes": 0,
        "isDeleted": False,
        "author": "5195193",
        "userScore": 0,
        "id": "243000862",
        "isClosed": False,
        "posts": 32,
        "link": "http://www.gazetaesportiva.net/noticia/2011/03/palmeiras/empresario-negocia-com-o-galo-para-trazer-ricardo-bueno-ao-verdao.html",
        "likes": 0,
        "message": "",
        "slug": "empresario_negocia_com_o_galo_para_trazer_ricardo_bueno_ao_verdao_gazeta_esportivanet",
        "createdAt": "2011-03-01T18:49:10"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:48",
      "message": "Mais um da srie bom e barato, OU SEJA, mais uma porcaria",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    },
    {
      "isJuliaFlagged": True,
      "isFlagged": False,
      "forum": "mightynest",
      "parent": None,
      "author": {
        "username": "facebook-1590383815",
        "about": "",
        "remote": {
          "domain": "facebook",
          "identifier": "1590383815"
        },
        "name": "Erin Hale",
        "url": "http://www.facebook.com/erinkhale",
        "id": "7730806",
        "profileUrl": "http://disqus.com/facebook-1590383815/",
        "emailHash": "d41d8cd98f00b204e9800998ecf8427e",
        "avatar": {
          "permalink": "http://disqus.com/api/users/avatars/facebook-1590383815.jpg",
          "cache": "http://mediacdn.disqus.com/uploads/users/773/806/avatar92.jpg?1281549413"
        },
        "isAnonymous": False,
      },
      "url": "http://mightynest.com/node/1834#comment-158476684",
      "isApproved": True,
      "dislikes": 0,
      "id": "158476684",
      "thread": {
        "category": "498055",
        "reactions": 0,
        "identifiers": [
          "node/1834"
        ],
        "forum": "mightynest",
        "title": "NEW! Lunchbots Trio and Container Set + GIVEAWAY!",
        "dislikes": 0,
        "isDeleted": False,
        "author": "4696869",
        "userScore": 0,
        "id": "232969726",
        "isClosed": False,
        "posts": 156,
        "link": "http://mightynest.com/node/1834",
        "likes": 32,
        "message": "",
        "slug": "introducing_lunchbots_trio_and_container_set_giveaway",
        "createdAt": "2011-02-17T17:21:12"
      },
      "points": 0,
      "createdAt": "2011-03-01T22:01:48",
      "message": "I'm a FB fan, and shared a link as well.",
      "isHighlighted": False,
      "isSpam": False,
      "isDeleted": False,
      "likes": 0
    }
]


def main():
    print "Sending fake comments"
    context = zmq.Context()
    while True:
        pub = context.socket(zmq.PUSH)
        pub.connect(SERVER)
        for i in xrange(0, random.randint(0, 100)):
            ip_address = generate_ip()
            result = geocode_addr(ip_address)
            if not result:
                continue
            if result['metro_code']:
                loc = result['metro_code']
            elif result['city']:
                loc = '%s, %s' % (result['city'].decode('latin1'), result['country_name'].decode('latin1'))
            else:
                loc = result['country_name']
            data = {
                'lat': result['latitude'],
                'lng': result['longitude'],
                'loc': loc,
                'post': anonymize(random.choice(messages), result['country_code']),
            }

            pub.send_json(data)
            gevent.sleep(0.1)
        pub.close()

if __name__ == '__main__':
    main()
