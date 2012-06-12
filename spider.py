#!/usr/bin/python
#coding=utf-8
"""
spider.py

This code is released under the following BSD license --

Copyright (c) 2012, solos
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of tinysearch nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY ITS CONTRIBUTORS ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Philip Semanchuk BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import gevent
from gevent import Timeout
from gevent import monkey
monkey.patch_all()

import logging
import urllib2
import robotparser
import re
from hashlib import md5
from datetime import date
from os import makedirs, error
from config import USERAGENT, TIMEOUT, LOGBASENAME, HTMLPATH, RETRY_TIMES

date = date.today()
tinyso_spider = urllib2.build_opener()
tinyso_spider.addheaders = [('User-agent', USERAGENT)]
logfilename = '%s.%s' % (str(date), LOGBASENAME)

logging.basicConfig(filename=logfilename, level=logging.INFO)

def fetch(url):
    with Timeout(TIMEOUT, Exception) as timeout:
        try:
            urlmd5 = md5(url).hexdigest()
            content = tinyso_spider.open(url).read()
            start = url.find(':') + 3
            end = url.find('/', 8)
            end = (end, len(url))[end <= 0]
            url_prefix = url[ start : end]
            htmlfile = open('%s/%s/%s' % (HTMLPATH, url_prefix, urlmd5), 'w')
            htmlfile.write(content)
            htmlfile.close()
        except urllib2.HTTPError, e:
            logging.info((urlmd5, e.code))
        except urllib2.URLError, e:
            logging.info((urlmd5, e.reason))
        except Exception as e:
            logging.info((urlmd5, 'Timeout'))
        else:
            logging.info((urlmd5, 'Ok'))

def get_url_prefix(url):
    '''get url prefix'''
    start = url.find(':') + 3
    end = url.find('/', 8)
    end = (end, len(url))[end <= 0]
    url_prefix = url[ start : end]
    return url_prefix

def path_init(urls):
    '''mkdir domains' dir if not exist'''

    dirs = []
    for url in urls:
        start = url.find(':') + 3
        end = url.find('/', 8)
        end = (end, len(url))[end <= 0]
        url_prefix = url[ start : end]
        dirs.append(url_prefix)
    dirs = list(set(dirs))
    for dir in dirs:
        try:
            makedirs('%s/%s' % (HTMLPATH, dir))
        except OSError, why :
            logging.info(str(why))
    return True

def findurl(content, url):
    '''find all url in content'''
    global out_urlmatch
    global in_urlmatch
    out_urlmatch = re.compile(r'(?:(?:href|src)=)(?:\"|\')?((?:http[s]{0,1}|ftp)://[a-zA-Z0-9][a-zA-Z0-9\\.\\-]*\.[a-zA-Z]{2,4}(?::\d+)?(?:/[a-zA-Z0-9\\.\\-~!@#$%^&amp;*+?:_/=<>]*))');
    in_urlmatch = re.compile(r'(?:(?:href|src)=)(?:\"|\')?(/[a-zA-Z0-9\\.\\.\\-~!@#$%^&amp;*+?:_/=<>]*)')
    #urlmatch = re.compile(r'href=(?:\"|\')?(.+?)(?:\"|\')');
    #url_prefix = url[:url.find('/', 8)]
    out_urls = list(set(out_urlmatch.findall(content)))
    in_urls = list(set(in_urlmatch.findall(content)))
    return url, url_prefix, in_urls, out_urls

if __name__ == '__main__':

    base_urls = ['http://www.google.com', 'http://www.wikipedia.org']
    path_init(base_urls)
    jobs = [ gevent.spawn(fetch, base_url) for base_url in base_urls ]
    gevent.joinall(jobs)
