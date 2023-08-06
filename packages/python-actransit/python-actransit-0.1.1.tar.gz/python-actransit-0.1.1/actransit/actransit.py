import functools
import requests
import urllib
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

API_Token = "C3310BE5BBB93CE82D142EADC87FD96B"


class BaseAPI:
    """Base wrapper for individual AC Transit APIs."""

    base_url = "https://api.actransit.org/transit"
    api = ""
    key = ""
    protobuf = ""
    url_truncate = False

    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return "BaseAPI()"

    def get_protobuf(self):
        """Gets protocol buffer file from the specified URL."""
        try:
            with urllib.request.urlopen(self.url) as response:
                self.protobuf.ParseFromString(response.read())
                protobuf_json = protobuf_to_dict(self.protobuf)
        except urllib.error.URLError as e:
            raise RuntimeError(e)

        return protobuf_json

    def get_json(self):
        """Gets JSON file prom the specified URL."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(e)

        return response.json()


def api_method(method):
    """Decorator for using method signatures to validate and make API calls."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Set method instances
        method(self, *args, **kwargs)
        # Include all other args into kwargs and add API token
        kwargs.update(zip(method.__code__.co_varnames[1:], args))
        kwargs.update({"token": self.key})
        # Remove kwargs specific to subclasses
        if "Route" in method.__qualname__:
            kwargs.pop("rt", None)
        if "Vehicle" in method.__qualname__:
            kwargs.pop("id", None)
        if "Stops" in method.__qualname__:
            kwargs.pop("stpid", None)

        # Create URL - check for truncated url param.
        kwargs_url = urllib.parse.urlencode(kwargs)
        if self.url_truncate:
            self.url = "{base_url}/{api}?{url_extn}".format(
                base_url=self.base_url, api=self.api, url_extn=kwargs_url
            )
        else:
            self.url = "{base_url}/{api}/{subdir}?{url_extn}".format(
                base_url=self.base_url,
                api=self.api,
                subdir=method.__name__,
                url_extn=kwargs_url,
            )

        # Generate API response
        if self.protobuf:
            return self.get_protobuf()
        else:
            return self.get_json()

    return wrapper


class Gtfs(BaseAPI):
    """API for General Transit Feed Specifications:
    https://api.actransit.org/transit/gtfs/"""

    api = "gtfs"

    def __repr__(self):
        return "ACTransit({})".format(self.__class__.__name__)

    @api_method
    def all(self):
        pass


class Gtfsrt(BaseAPI):
    """API for real time General Transit Feed Specifications:
    https://api.actransit.org/transit/gtfsrt/"""

    api = "gtfsrt"
    protobuf = gtfs_realtime_pb2.FeedMessage()

    def __repr__(self):
        return "ACTransit({})".format(self.__class__.__name__)

    @api_method
    def alerts(self):
        pass

    @api_method
    def tripupdates(self):
        pass

    @api_method
    def vehicles(self):
        pass


class Route(BaseAPI):
    """API for route information, such as direction, trips, and
    vehicles on the route:
    https://api.actransit.org/transit/routes/
    https://api.actransit.org/transit/route/{rt}/"""

    api = "route"

    def __repr__(self):
        return "ACTransit({})".format(self.__class__.__name__)

    @api_method
    def all(self):
        self.api = "routes"
        self.url_truncate = True

    @api_method
    def directions(self, rt):
        self.api = "route/{}".format(rt)
        self.url_truncate = True

    @api_method
    def trips(self, rt, direction=""):
        self.api = "route/{}".format(rt)
        self.url_truncate = True

    @api_method
    def tripsestimates(self, rt, fromStopId="", toStopId=""):
        self.api = "route/{}".format(rt)
        self.url_truncate = True

    @api_method
    def tripsinstructions(self, rt, direction=""):
        self.api = "route/{}".format(rt)
        self.url_truncate = True

    @api_method
    def vehicles(self, rt):
        self.api = "route/{}".format(rt)
        self.url_truncate = True


class ACTRealtime(BaseAPI):
    """API to retrieve real time information about detours,
    predictions, service bulletins and vehicles:
    https://api.actransit.org/transit/actrealtime/"""

    api = "actrealtime"

    def __repr__(self):
        return "ACTransit({})".format(self.__class__.__name__)

    @api_method
    def detour(self, rt="", rtdir=""):
        pass

    @api_method
    def direction(self, rt):
        pass

    @api_method
    def line(self):
        pass

    @api_method
    def locale(self):
        pass

    @api_method
    def pattern(self, pid="", rt=""):
        pass

    @api_method
    def prediction(self, stpid="", rt="", vid="", top="", tmres=""):
        pass

    @api_method
    def time(self, unixTime=""):
        pass

    @api_method
    def servicebulletin(self, rt="", rtdir="", stpid=""):
        pass

    @api_method
    def stop(self, rt="", dir="", stpid=""):
        pass

    @api_method
    def vehicle(self, vid="", rt="", tmres=""):
        pass


class Vehicle(BaseAPI):
    """API to retrieve vehicle information by ID:
    https://api.actransit.org/transit/vehicle/{id}/"""

    api = "vehicle"

    def __repr__(self):
        return "ACTransit({})".format(self.__class__.__name__)

    @api_method
    def id(self, id):
        self.api = "vehicle/{}".format(id)
        self.url_truncate = True


class Stops(BaseAPI):
    """API to retrieve information about stops -
    such as routes and real-time predictions:
    https://api.actransit.org/transit/stops/
    https://api.actransit.org/transit/stops/{stpid}/"""

    api = "stops"

    def __repr__(self):
        return "ACTransit({})".format(self.__class__.__name__)

    @api_method
    def all(self):
        self.url_truncate = True

    @api_method
    def predictions(self, stpid):
        self.api = "stops/{}".format(stpid)
        self.url_truncate = False

    @api_method
    def routes(self, stpid):
        self.api = "stops/{}".format(stpid)
        self.url_truncate = False


class ACTransit:
    """Wrapper for the AC Transit API."""

    def __init__(self, key=API_Token):
        """Initialize the individual APIs with the API key."""
        args = (key,)
        self.gtfs = Gtfs(*args)
        self.gtfsrt = Gtfsrt(*args)
        self.route = Route(*args)
        self.actrealtime = ACTRealtime(*args)
        self.vehicle = Vehicle(*args)
        self.stops = Stops(*args)

    def __repr__(self):
        return "ACTransit()"
