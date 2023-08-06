python-actransit
================

A simple Alameda-Contra Costa Transit District (`AC Transit <http://www.actransit.org/>`__) API wrapper.

License: `MIT <https://en.wikipedia.org/wiki/MIT_License>`__.

Installation
------------

::

    pip install python-actransit

API Examples
------------
Make an instance of the ``ACTransit`` class.

.. code:: python

    from actransit import ACTransit
    ac_transit = ACTransit()


Get vehicle information and positions from a `GTFS <https://gtfs.org/>`__ real-time feed.

.. code:: python

    realtime_vehicles = ac_transit.gtfsrt.vehicles()
    print(realtime_vehicles)

    {'entity': [{'id': '1',
                'vehicle': {'position': {'bearing': 116.0,
                                        'latitude': 37.80388259887695,
                                        'longitude': -122.276611328125,
                                        'speed': 0.0},
                            'timestamp': 1579463770,
                            'trip': {'route_id': '19',
                                    'schedule_relationship': 0,
                                    'trip_id': '751100010'},
                            'vehicle': {'id': '5020'}}},
                # ...
                ],
    'header': {'gtfs_realtime_version': '1.0',
                'incrementality': 0,
                'timestamp': 1579463788}}

Get information for any existing schedule: current, past and future.

.. code:: python

    existing_schedules = ac_transit.gtfs.all()
    print(existing_schedules)

    [{'BookingId': '1912WR',
    'EarliestServiceDate': '2019-12-14T00:00:00',
    'LatestServiceDate': '2020-03-28T00:00:00',
    'UpdatedDate': '2019-12-11T07:45:25.96'},
    {'BookingId': '1908FA',
    'EarliestServiceDate': '2019-08-10T00:00:00',
    'LatestServiceDate': '2019-12-14T00:00:00',
    'UpdatedDate': '2019-08-01T15:20:19.587'},
    # ...
    ]

Get trip information for a bus route (e.g. route 212).

.. code:: python

    route_212 = ac_transit.route.trips(rt=212)
    print(route_212)

    {'RouteId': '212', 'Name': '212', 'Description': 'Fremont Blvd. - Pacific Commons'}


Get real-time predictions for a bus stop (e.g. stop ID 51331).

.. code:: python

    predict_stop = ac_transit.actrealtime.prediction(stpid=51331)
    print(predict_stop)

    {'bustime-response': {'prd': [{'des': 'Downtown Berkeley',
                               'dly': False,
                               'dstp': 1490,
                               'dyn': 0,
                               'geoid': '3539',
                               'prdctdn': '1',
                               'prdtm': '20200122 10:47',
                               'rid': '604',
                               'rt': '6',
                               'rtdd': '6',
                               'rtdir': 'To Downtown Berkeley',
                               'schdtm': '20200122 10:47',
                               'seq': 7,
                               'stpid': '51331',
                               'stpnm': 'Telegraph Av + 29th St',
                               'tablockid': '6002',
                               'tatripid': '6619563',
                               'tmstmp': '20200122 10:45',
                               'tripdyn': 0,
                               'tripid': '743320020',
                               'typ': 'A',
                               'vid': '1350',
                               'zone': ''},
                               # ...
                              ]}}

Get information for every AC Transit bus stop.

.. code:: python

    all_stops = ac_transit.stops.all()
    print(all_stops)

    [{'Latitude': 37.7773372,
    'Longitude': -122.2630574,
    'Name': 'Sherman St:Buena Vista Av',
    'ScheduledTime': None,
    'StopId': 52304},
    {'Latitude': 37.9262186,
    'Longitude': -122.3169712,
    'Name': 'Cutting Blvd:Ohlone Greenway (Del Norte BART)',
    'ScheduledTime': None,
    'StopId': 52306},
    # ...
    ]

Every method in ``ACTransit``
-----------------------------

.. code:: python

    from actransit import ACTransit
    ac_transit = ACTransit()


    # GTFS
    ac_transit.gtfs.all()

    # GTFSRT
    ac_transit.gtfsrt.vehicles()
    ac_transit.gtfsrt.alerts()
    ac_transit.gtfsrt.tripupdates()

    # Routes
    ac_transit.route.all()
    ac_transit.route.directions(rt)  # route ID (type int or str)
    ac_transit.route.trips(rt, direction='')  # route ID (type int or str) and direction (type str)
    ac_transit.route.tripsestimates(rt, fromStopID='', toStopID='') # route ID and stop ID (both type int or str)
    ac_transit.route.tripsinstructions(rt, direction='')  # route ID (type int or str) and direction (type str)
    ac_transit.route.vehicles(rt)  # route ID (type int or str)

    # AC Transit real-time
    ac_transit.actrealtime.detour(rt='', rtdir='')   # route ID (type int or str) and route direction (type str)
    ac_transit.actrealtime.direction(rt)  # route ID (type int or str)
    ac_transit.actrealtime.line()
    ac_transit.actrealtime.locale()
    ac_transit.actrealtime.pattern(pid='', rt='')  # PID and route ID (both type int or str)
    ac_transit.actrealtime.prediction(stpid='', rt='', vid='', top='', tmres='')  # stop ID, route ID, vehicle ID,
    # max items return, time resolution ('s', 'm')  (all type int or str, except tmres, which takes str)
    ac_transit.actrealtime.time(unixTime='')  # UNIX time (type int or str)
    ac_transit.actrealtime.servicebulletin(rt='', rtdir='', stpid='')  # route ID, route direction, and stop ID
    # (all type int or str, except rtdir, which takes str)
    ac_transit.actrealtime.stop(rt='', dir='', stpid='')  # route ID, route direction, and stop ID
    # (all type int or str, except dir, which takes str)
    ac_transit.actrealtime.vehicle(vid='', rt='', tmres='') # vehicle ID, route ID, and time resolution
    # (all type int or str, except tmres, which takes str)

    # Vehicle
    ac_transit.vehicle.id(id)  # vehicle ID (type int or str)

    # Stops
    ac_transit.stops.all()
    ac_transit.stops.predictions(stpid)  # stop ID (type int or str)
    ac_transit.stops.routes(stpid)  # stop ID (type int or str)

Support
-------

If you find any bug or you want to propose a new feature, please use the `issues tracker <https://github.com/irahorecka/python-actransit/issues>`__. I'll be happy to help!
