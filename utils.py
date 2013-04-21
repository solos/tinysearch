#!/usr/bin/python
#coding=utf-8

import lxml.html
from lxml.html.clean import Cleaner
import jieba
import config
from bitarray import bitarray

cleaner = Cleaner()


def extracter(content):
    '''extracte the content of html'''

    try:
        content = cleaner.clean_html(content)
        text = lxml.html.fromstring(content)
        return text.text_content().format()
    except Exception, e:
        print e
        return u''


def split(content):
    '''split the content to words'''

    try:
        return list(jieba.cut(content, cut_all=False))
    except Exception, e:
        print e
        return []


def index(content):

    if not isinstance(content, unicode):
        content = content.decode('utf8')
    bitarr = 51200 * bitarray('0')
    words = set(split(extracter(content)))
    for word in words:
        try:
            wid = config.feature_words[word]
            bitarr[wid] = True
        except Exception:
            continue
    return bitarr


def get_url_prefix(url):
    '''get url prefix'''
    start = url.find(':') + 3
    end = url.find('/', 8)
    end = (end, len(url))[end <= 0]
    url_prefix = url[start:end]
    return url_prefix


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
