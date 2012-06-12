#!/usr/bin/python
#coding=utf-8
"""
is_ambiguous.py

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

import redis
from config import DICT_FILE
import codecs
import db
from time import time

def init():
    dict_file = codecs.open(DICT_FILE, 'r', 'utf-8')
    for line in dict_file.readlines():
        line = line[:-1]
        if len(line) == 2:
            db.bitmap_rds.setbit(ord(line[0]), ord(line[1]), 1)
    dict_file.close()

def if_conficit(Ustr):
    length = len(Ustr)
    if length < 3:
        return False
    for i in xrange(0, length - 2):
        if db.bitmap_rds.getbit(ord(Ustr[i]), ord(Ustr[i+1])) and db.bitmap_rds.getbit(ord(Ustr[i+1]), ord(Ustr[i+2])):
            return True
        else:
            return False

def test(Ustr):
    return if_conficit(Ustr)

if __name__ == '__main__':
    print time()
    init()
    print time()
    Ustr = u'计算计'
    print time()
    for i in xrange(1, 10000):
        if_conficit(Ustr)
    print time()
