"""Performs requests to the Amap Distance Matrix API."""


strategy = {"tolls": 13, "highways": 14, "congestion": 12}


def address_to_coord(client, address):
    payload = {"address": address, "output": "JSON"}
    coord = client._request("/v3/geocode/geo", payload)
    if coord.json()["status"] == "1":
        return coord.json()["geocodes"][0]["location"]


def distance_matrix(client, origin, destination,
                    mode=None, avoid=None, province=None, number=None,
                    transit_routing_preference=None, city=None, cityd=None):
    """ Gets travel distance and time for a matrix of origins and destinations.

    :param origin: One location longitude/latitude values,
        from which to calculate distance and time.
    :type origin: a single location, where a location is a string

    :param destination: One location longitude/latitude values,
        from which to calculate distance and time.
    :type destination: a single location, where a location is a string

    :param mode: Specifies the mode of transport to use when calculating
        directions. Valid values are "driving", "walking", "transit" or
        "bicycling".
    :type mode: string

    :param avoid: Indicates that the calculated route(s) should avoid the
        indicated features. Valid values are "tolls", "highways" or "ferries".
    :type avoid: string

    :param departure_time: Specifies the desired time of departure.
    :type departure_time: int or datetime.datetime

    :param transit_mode: Specifies one or more preferred modes of transit.
        This parameter may only be specified for requests where the mode is
        transit. Valid values are "bus", "subway", "train", "tram", "rail".
        "rail" is equivalent to ["train", "tram", "subway"].
    :type transit_mode: string or list of strings

    :param transit_routing_preference: Specifies preferences for transit
        requests. Valid values are "less_walking" or "fewer_transfers".
    :type transit_routing_preference: string

    :param region: Specifies the prefered region the geocoder should search
        first, but it will not restrict the results to only this region. Valid
        values are a ccTLD code.
    :type region: string

    :rtype: matrix of distances. Results are returned in rows, each row
        containing one origin paired with each destination.
    """

    params = {
        "origin": origin,
        "destination": destination,
        "output": "JSON"
    }
    if mode:
        # NOTE(broady): the mode parameter is not validated by the Maps API
        # "driving", "walking", "transit" or "bicycling".
        if mode == "walking":
            su = client._request("/v3/direction/walking", params)
        elif mode == "bicycling":
            su = client._request("/v4/direction/bicycling", params)
        elif mode == "transit":
            if city:
                params["city"] = city
            else:
                raise ValueError("departure city must be specified.")
            if cityd:
                params["cityd"] = cityd
            if transit_routing_preference:
                if transit_routing_preference == "less_walking":
                    params["strategy"] = 3
                elif transit_routing_preference == "fewer_transfers":
                    params["strategy"] = 2
                else:
                    params["strategy"] = 0

            su = client._request("/v3/direction/transit/integrated", params)
        elif mode == "driving":
            if avoid:
                if avoid not in ["tolls", "highways", "congestion", "restriction"]:
                    raise ValueError("Invalid route restriction.")
                params["strategy"] = strategy.get(avoid, 10)
            else:
                params["strategy"] = 10
            if number and province:
                params["number"] = number
                params["province"] = province
            su = client._request("/v3/direction/driving", params)
        else:
            raise ValueError("Invalid travel mode.")

        return su.json()
