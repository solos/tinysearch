#!/usr/bin/python
#coding=utf-8
"""
ander.py

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

from config import DOC_TOTAL, TOTAL_SET
import db
from collections import defaultdict

def ander(word_list):
    doc_id_sets = defaultdict(set)

    for word in word_list:
        for doc_id in xrange(0, DOC_TOTAL):
            if db.index_rds.getbit(word, doc_id) == 1:
                doc_id_sets[word].add(doc_id)

    comm_doc_id_set = TOTAL_SET
    for word in word_list:
        comm_doc_id_set &= doc_id_sets[word]
    comm_doc_id_list = list(comm_doc_id_set)
    return comm_doc_id_list

if __name__ == '__main__':
    pass

