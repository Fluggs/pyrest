#!/usr/bin/env python3

import json
import urllib.request
import urllib.error


class Client:
    def __init__(self, url):
        # build api url
        self.base_url = Client._normalize_url_part(url)
        self.url_appendix = ""
        if not self.base_url.startswith("http://") and not self.base_url.startswith("https://"):
            self.base_url = "http://" + self.base_url

        self.decoder = json.JSONDecoder()
        self.encoder = json.JSONEncoder()

    @staticmethod
    def _normalize_url_part(part):
        """
        Normalizes a URL part, i.e. removes "/" at the beginning and adds one at the end
        *TODO* urlencode
        :param part: URL part to normalize
        :return:
        """
        while True:
            if not part.startswith("/"):
                break
            part = part[1:]

        while True:
            if not part.endswith("/"):
                break
            part = part[:-1]

        if part == "":
            return part
        return part + "/"

    def set_url_appendix(self, s):
        """
        Sets an appendix for the host URL (useful for things that don't change like authentication)
        :param s: appendix
        :return: None
        """
        s = Client._normalize_url_part(s)
        self.base_url += s

    def parse_response(self, response):
        """
        Parses a json response from the API.
        :param response: response to parse
        :return: representation of the json response
        """
        return self.decoder.decode(response)

    def parse_request_data(self, data):
        """
        Parses a dict to urlencoded json
        :param data:
        :return:
        """
        if data is None:
            return None
        return self.encoder.encode(data)

    def url(self, endpoint=""):
        """
        Build the URL with url, appendix and endpoint
        :param endpoint: endpoint, defaults to ""
        :return: built URL
        """
        return self.base_url + self.url_appendix + endpoint

    def make_request(self, endpoint, data=None, method="GET"):
        """
        does the http and json part
        :param method: http method ("GET", "POST" etc)
        :param endpoint: REST resource / end point
        :param data: dict that is being sent
        :return: parsed response
        """
        endpoint = Client._normalize_url_part(endpoint)
        if data is not None:
            data = self.parse_request_data(data)
            data = data.encode("utf-8")
        request = urllib.request.Request(self.url(endpoint), data=data, method=method)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            response = e
        response = self.parse_response(response.read().decode("utf-8"))
        return response

