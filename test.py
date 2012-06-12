#!/usr/bin/python
#coding=utf-8
"""
test.py

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

from spider import path_init, fetch
import gevent
from gevent import Timeout
from gevent import monkey
monkey.patch_all()

from lynx import lynx
import spliter
from indexer import indexer
from sorter import sorter
from ander import ander

if __name__ == '__main__':

    base_urls = ['http://www.google.com', 'http://www.wikipedia.org']
    print '*** 0. mkdir dir to store the html files ***'
    path_init(base_urls)
    print '*** 1. tinysearch spider starts ***'
    jobs = [ gevent.spawn(fetch, base_url) for base_url in base_urls ]
    gevent.joinall(jobs)
    print '*** 2. lynx html in order to get the content ***'
    lynx('html')
    print '*** 3. load spliter dict ***'
    dic = spliter.init()
    print '*** 4. index content and return doc_id ***'
    print "*** 5. doc_id is %s ***" % ( indexer(dic, './test/', 'test.html') )
    word_list = [u'百科']
    print '*** 6. get common doc_id list ***'
    doc_id_list = ander(word_list)
    print doc_id_list
    print '*** 7. sort the result ***'
    print sorter(word_list, doc_id_list)
