# coding=utf-8

import requests
import logging
import dns.resolver


class Client:

    """
    from fncaller.client import Client
    c = Client(search_auth="",auth_header="")
    resp = c.call("os_scan.ttl",ip="1.1.1.1")
    print(resp)
    """

    baseurl = "http://your.fn.server/rpc"
    search_auth = ""
    auth_header = ""

    def __init__(self, **kwargs):
        self.search_auth = kwargs.get("search_auth")
        if kwargs.get("baseurl", "") != "":
            self.baseurl = kwargs.get("baseurl")

        if kwargs.get("auth_header", "") != "":
            self.auth_header = kwargs.get("auth_header")

    def buildURL(self, name, **kwargs):
        url = "%s?auth=%s&name=%s" % (self.baseurl, self.search_auth, name)
        params = []
        for name, value in kwargs.items():
            if name != "body":
                params.append("arg_%s=%s" % (name, value))
        return url + "&" + "&".join(params)

    def buildHeaders(self):
        return {
            "rpc-auth": self.auth_header
        }

    def __call__(self, name, **kwargs):
        body = kwargs.get("body", "")
        url = self.buildURL(name, **kwargs)
        logging.debug(" url : %s", url)
        if body == "":
            return requests.get(self.buildURL(name, **kwargs), headers=self.buildHeaders())
        else:
            return requests.post(self.buildURL(name, **kwargs), body=body, headers=self.buildHeaders())

    def call(self, name, **kwargs):
        resp = self(name, **kwargs)
        if resp.status_code == 200:
            return resp.text
        else:
            return ""


def getRpcServers(domain=""):
    records = dns.resolver.query(domain, 'A')
    return [record.address for record in records]
