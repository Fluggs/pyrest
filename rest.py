#!/usr/bin/env python3

import json
import urllib.request
import urllib.error


class Client:
    def __init__(self, url, username):
        # build api url with username
        self.base_url = url
        if not self.base_url.endswith("/"):
            self.base_url += "/"
        if not self.base_url.startswith("http://"):
            self.base_url = "http://" + self.base_url
        self.base_url += username
        self.base_url += "/"

        self.decoder = json.JSONDecoder()
        self.encoder = json.JSONEncoder()

    @staticmethod
    def normalize_url_part(part):
        """
        Normalizes a url part, i.e. removes "/" at the end and urlencodes it (not impl yet)
        :param part:
        :return:
        """
        if part.startswith("http:"):
            part = part[5:]
        elif part.startswith("https:"):
            part = part[6]
        while True:
            if not part.startswith("/"):
                break
            part = part[1:]

        while True:
            if not part.endswith("/"):
                break
            part = part[:-1]

        return part

    def make_request(self, host, endpoint, data=None, headers={}, method="GET"):
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
