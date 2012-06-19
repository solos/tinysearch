#!/bin/bash
#{ 
#   'base_env': 
#   {
#	'release' : 'ubuntu 10.04', 
#	'python' : '2.6.5' 
#   }, 

#   'additional_pkg': 
#   { 
#	'git': '1.7.10',
#	'mysql': '5.1', 
#	'lynx': '2.8.8',
#	'pip': '1.0', 
#	'python-mysql': '1.2.3', 
#	'robotexclusionrulesparser':'1.4.0',
#	'kyotocabinet': '1.2.30', 
#	'kyotocabinet-python': 'kyotocabinet-python-legacy-1.18',
#	'redis': '2.6.0-rc4',
#	'redis-python': '2.4.13',
#	'dnsmasq': '2.52'
#   }
#}

##################################################################################################################
# notice: if you use other linux releases, please replace the apt-get with the right package manager command.    #
#   the redis-python 2.4.13 does not support redis 2.6.0 's bitcount command so i add it and you can clone it    #
#   from github by using git clone ssh://github.com/solos/redis-py or you can modify it manually(client.py).     #
##################################################################################################################

mkdir ./pkgs && cd pkgs

echo 'git'
sudo apt-get install git-core

echo 'mysql'
sudo apt-get install mysql-server-5.1 

echo 'lynx'
sudo apt-get install lynx

echo 'python-setuptools'
sudo apt-get install python-setuptools

echo 'python-mysql'
sudo pip install mysql-python

echo 'robotexclusionrulesparser'
wget 'http://nikitathespider.com/python/rerp/robotexclusionrulesparser-1.4.0.py'

echo 'kyotocabinet'
wget 'http://fallabs.com/kyotocabinet/pkg/kyotocabinet-1.2.30.tar.gz'
tar xf kyotocabinet-1.2.30.tar.gz && cd kyotocabinet-1.2.30
./configure --prefix=/usr/local/
sudo make
sudo make install
cd ..

echo 'kyotocabinet-python'
wget 'http://fallabs.com/kyotocabinet/pythonlegacypkg/kyotocabinet-python-legacy-1.18.tar.gz'
tar xf kyotocabinet-python-legacy-1.18.tar.gz && cd kyotocabinet-python-legacy-1.18
sudo python setup install
cd ..

echo 'redis'
wget 'http://redis.googlecode.com/files/redis-2.6.0-rc4.tar.gz'
tar xf redis-2.6.0-rc4.tar.gz && cd redis-2.6.0-rc4
sudo make
sudo make install
cd ..

echo 'redis-python'
git clone ssh://github.com/solos/redis-py.git
cd redis-py 
sudo python setup.py install
cd ..

echo 'dnsmasq'
sudo apt-get install dnsmasq
