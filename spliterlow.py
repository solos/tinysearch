#!/usr/bin/python
#coding=utf-8
"""
spliterlow.py

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

import codecs
import time
import re
from collections import defaultdict
from config import DICT_FILE, MAX_LENGTH

def init():
    '''load dict_file and init dict'''
    dict_file = codecs.open(DICT_FILE, 'r', 'utf-8')
    dic = defaultdict(list)
    for line in dict_file.readlines():
        line = line[:-1]
        dic[line[0:2]].append(line[2:])
    dict_file.close()
    return dic

def inDict(Ustr, dic):
    '''check if Ustr in dic'''
    return Ustr[2:] in dic[Ustr[0:2]]

def cut(content):
    '''cut content to fragments'''
    uStrList = re.sub(u"""，|,|。|.|！|!|:|：|《|》|<|>|'|"|||…|？|\?|、|\||“|”|‘|’|；|—|（|）|·|\(|\)|　"""," ",content).split()
    return uStrList

def split(inUstr, dic, maxLen=5):
    '''split inUstr to words'''
    outUstr = u''
    while inUstr:
        inLen = len(inUstr)
        wlen = (inLen, maxLen)[inLen > maxLen]
        word = inUstr[:wlen]
        for length in xrange(wlen, 0, -1):
            if inDict(inUstr[:length], dic) or length == 1:
                outUstr = "%s%s%s" % (outUstr, u' ', inUstr[:length])
                inUstr = inUstr[length:]
                break
    return outUstr

if __name__ == '__main__':
    dic=init()
    content = codecs.open('./test/test.txt', 'r', 'utf-8').read()
    print len(content)
    inUstrList = cut(content)
    print time.time()
    for inUstr in inUstrList:
        split(inUstr, dic, maxLen=5)
    print time.time()
