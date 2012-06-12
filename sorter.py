#!/usr/bin/python
#coding=utf-8
"""
sorter.py

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

from operator import itemgetter
from collections import defaultdict
from math import log10
import db
from config import DOC_TOTAL

def sorter(word_list, doc_id_list):
    doc_weight = defaultdict(tuple)

    idf_dic = defaultdict(tuple)
    for word in word_list:
        word_idf = log10( DOC_TOTAL / (db.index_rds.bitcount(word) + 1) )
        idf_dic[word] = word_idf

    for doc_id in  doc_id_list:
        tf_dic_str = db.tf_dic_db.get(doc_id)
        if not tf_dic_str:
            tf_dic_str = u'{}'
        tf_dic = eval(tf_dic_str)
        for word in word_list:
            #word = unicode(word, 'utf-8')
            db.index_rds.setbit(word, doc_id, 1)
            doc_weight[doc_id] = tf_dic[word] * idf_dic[word]

    return sorted(doc_weight.iteritems(), key=itemgetter(1), reverse=True)

if __name__ == '__main__':
    '''
    word_list = ['你好', '世界']
    doc_id_list = [1, 2, 3]
    sorter(word_list, doc_id_list)
    '''
