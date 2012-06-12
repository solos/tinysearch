#!/usr/bin/python
#coding=utf-8
"""
indexer.py

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

from os import popen
from lynx import lynx
import spliter
import logging
from collections import defaultdict
import db

def indexer(dic, path, filename):
    '''index the file'''
    tf_dic = defaultdict(tuple)
    content = lynx( "%s/%s" % (path, filename) )
    content = unicode(content, 'utf-8')
    
    urlmd5 = filename
    doc_id = db.doc_id_db.get(urlmd5)
    if not doc_id:
        doc_id_count = db.doc_id_db.count()
        if db.doc_id_db.set(urlmd5, doc_id_count):
            doc_id = db.doc_id_db.set(urlmd5, doc_id_count)
    inUstrList = spliter.cut(content)
    outUstr = ''
    for inUstr in inUstrList:
        #outUstrList.append( spliter.split(inUstr, dic, maxLen=5).split(' ') )
        outUstr = '%s %s' % ( outUstr, spliter.split(inUstr, dic, maxLen=5) )
    outList = list( set(outUstr.split(' ')) )
    for word in outList:
        db.index_rds.setbit(word, doc_id, 1)

    for word in outList:
        tf_dic[word] = outUstr.count(word)
    db.tf_dic_db.set(doc_id, unicode(dict(tf_dic)))

    return True


if __name__ == '__main__':
    dic = spliter.init()
    indexer(dic, './test', 'test.html')
