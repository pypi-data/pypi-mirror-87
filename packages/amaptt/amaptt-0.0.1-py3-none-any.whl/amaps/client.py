"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

import requests
import amaps


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
            raise amaps.exceptions.Timeout()
        except Exception as e:
            raise amaps.exceptions.TransportError(e)
        return response

    def _append_key(self, params):
        if self.key:
            params["key"] = self.key
            return params

        raise ValueError("Must provide API key for this API. It does not accept "
                         "enterprise credentials.")

