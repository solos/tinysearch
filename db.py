#!/usr/bin/python
#coding=utf-8
"""
db.py

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

import MySQLdb
from hashlib import md5
from datetime import date
import kyotocabinet
from config import DB, DB_HOST, DB_USER, DB_PASSWD, DB_CHARSET, DB_PATH, RDS_HOST, RDS_PORT, INDEX_RDS_DB, IDF_RDS_DB, BITMAP_RDS_DB
import logging
import redis

today_date = date.today()

conn = MySQLdb.connect(db=DB, host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, charset=DB_CHARSET)
cursor = conn.cursor()

domain_db = kyotocabinet.DB()
if not domain_db.open("%sdomain.kch" % DB_PATH, kyotocabinet.DB.OWRITER | kyotocabinet.DB.OCREATE):
    logging.info( str(domain_db.error()) )

url_db = kyotocabinet.DB()
if not url_db.open("%surl.kch" % DB_PATH, kyotocabinet.DB.OWRITER | kyotocabinet.DB.OCREATE):
    logging.info( str(url_db.error()) )

doc_id_db = kyotocabinet.DB()
if not doc_id_db.open("%sdoc_id.kch" % DB_PATH, kyotocabinet.DB.OWRITER | kyotocabinet.DB.OCREATE):
    logging.info( str(doc_id_db.error()) )

tf_dic_db = kyotocabinet.DB()
if not tf_dic_db.open("%stf_dic.kch" % DB_PATH, kyotocabinet.DB.OWRITER | kyotocabinet.DB.OCREATE):
    logging.info( str(tf_dic_db.error()) )

index_rds = redis.StrictRedis(host=RDS_HOST, port=RDS_PORT, db=INDEX_RDS_DB)
idf_rds = redis.StrictRedis(host=RDS_HOST, port=RDS_PORT, db=IDF_RDS_DB)
bitmap_rds = redis.StrictRedis(host=RDS_HOST, port=RDS_PORT, db=BITMAP_RDS_DB)

def crt_tb(cursor):
    '''create table url'''
    result = cursor.execute('''create table if not exists url(id int unsigned not null primary key auto_increment, domain_id int unsigned not null default 0, status tinyint unsigned not null default 0, frequency tinyint unsigned not null default 0, last_date date not null default 0, next_date date not null default 0, md5 char(16) not null default '') engine=MyISAM, CHARACTER SET utf8 COLLATE utf8_general_ci ;''')
    if result:
        return True
    else:
        return False

def get_domain_id(domain):
    '''get domain_id from kv db '''
    domain_id = domain_db.get(domain)
    if domain_id:
        return domain_id
    else:
        domain_id = domain_db.count() + 1
        domain_db.set(domain_id, domain)
        return domain_id

def is_in_urldb(url):
    '''return whether url is in url_db'''
    urlmd5 = md5(url).hexdigest()
    url = url_db.get(urlmd5)
    if url:
        return True
    else:
        return False

def inst_url(cursor, urls):
    '''insert url into mysql db and kv db'''
    for url in urls:
        urlmd5 = md5(url).hexdigest()
        domain_id = get_domain_id(domain)
        result = cursor.execute('''insert into url(domain_id, md5) value(%s, %s)''', (domain_id, urlmd5))
        if result:
            url_db.set(urlmd5, url)
        else:
            continue
    return True


def selt_url(cursor, date):
    result = cursor.execute('''select md5 from url where next_date == %s''', (today_date))
    if result:
        urlmd5s = result.fetchall()
        urls = []
        for urlmd5 in urlmd5s:
            urls.append(url_db.get(urlmd5))
        return urls
    else:
        return []

if __name__ == '__main__':
    crt_tb(cursor)
    domain_db.close()
    url_db.close()
    doc_id_db.close()
    tf_dic_db.close()
    cursor.close()
    conn.close()
