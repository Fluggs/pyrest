#!/usr/bin/env python3

import json
import urllib.request, urllib.error

host = None

def make_request(host, endpoint, data=None, headers={}, method="GET"):
    # build URL
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
    if host.endswith("/"):
        host = host[:-1]
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]
    if endpoint.endswith("/"):
        endpoint = endpoint[:-1]

    url = host + "/" + endpoint

    # build data
    if data is not None:
        encoder = json.JSONEncoder()
        data = encoder.encode(data)
        data = data.encode("utf-8")

    req = urllib.request.Request(url, data, headers=headers, method=method)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        return(e)
    return response
    
def main(endpoint, data=None, method="GET", headers={}):
    global host
    
    return make_request(host, endpoint, data, headers, method)
