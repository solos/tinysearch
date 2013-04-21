#!/usr/bin/python
#coding=utf-8

import urllib2
import httplib
import socket
import dns.resolver
import dns.exception
import config


def custom_resolver(host):
    custom_resolver = dns.resolver.Resolver()
    custom_resolver.nameservers = config.NAMESERVERS
    try:
        answer = custom_resolver.query(host)
        return answer[0].address
    except dns.exception.DNSException:
        return ''


class CustomHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        self.sock = socket.create_connection((
            custom_resolver(self.host), self.port), self.timeout)


class CustomHTTPSConnection(httplib.HTTPSConnection):
    def connect(self):
        self.sock = socket.create_connection((
            custom_resolver(self.host), self.port), self.timeout)


class CustomHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return self.do_open(CustomHTTPConnection, req)


class CustomHTTPSHandler(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(CustomHTTPSConnection, req)


_spider = urllib2.build_opener(CustomHTTPHandler, CustomHTTPSHandler)
_spider.addheaders = [('User-agent', config.USERAGENT)]
urllib2.install_opener(_spider)

if __name__ == '__main__':

    url = "http://www.baidu.com"
    request = _spider.open(url)
    response = request.read()
    print response
