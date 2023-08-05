"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

import requests
import amaptt
import functools

_DEFAULT_BASE_URL = "https://restapi.amap.com"


class Client(object):
    """Performs requests to the Google Maps API web services."""

    def __init__(self, key=None, timeout=None, requests_kwargs=None, base_url=_DEFAULT_BASE_URL):
        """
        """
        if not key:
            raise ValueError("Must provide API key or enterprise credentials "
                             "when creating client.")
        self.session = requests.Session()
        self.key = key
        if timeout:
            raise ValueError("Specify either timeout, or connect_timeout "
                             "and read_timeout")
        else:
            self.timeout = timeout
        self.requests_kwargs = requests_kwargs or {}
        self.base_url = base_url

    def request(self, url, params):

        # Default to the client-level self.requests_kwargs, with method-level
        # requests_kwargs arg overriding.

        params = self._append_key(params)
        print(params)
        url2 = self.base_url + url
        print(url2)
        try:
            # response = self.session.get(url2, params)
            response = self.session.get(url2, params=params)
            print(response.text)
        except requests.exceptions.Timeout:
            raise amaptt.exceptions.Timeout()
        except Exception as e:
            raise amaptt.exceptions.TransportError(e)
        return response

    def _append_key(self, params):
        if self.key:
            params["key"] = self.key
            return params

        raise ValueError("Must provide API key for this API. It does not accept "
                         "enterprise credentials.")


from amaps.distance_matrix import distance_matrix, address_to_coord


def make_api_method(func):
    """
    Provides a single entry point for modifying all API methods.
    For now this is limited to allowing the client object to be modified
    with an `extra_params` keyword arg to each method, that is then used
    as the params for each web service request.

    Please note that this is an unsupported feature for advanced use only.
    It's also currently incompatibile with multiple threads, see GH #160.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args[0]._extra_params = kwargs.pop("extra_params", None)
        result = func(*args, **kwargs)
        try:
            del args[0]._extra_params
        except AttributeError:
            pass
        return result

    return wrapper


Client.distance_matrix = make_api_method(distance_matrix)
Client.address_to_coord = make_api_method(address_to_coord)
