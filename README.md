tinysearch 台泥搜
======================

关于
-----------------

    tinysearch(台泥搜)是一个关于搜索的毕业设计项目，起初是为了给歌词迷(http://geci.me)加一个歌词全文检索功能，后来临近
    毕业选了一个与搜索相关的毕业设计，掉到了这个坑里。台泥搜使用python语言编写，功能相当少，性能相当烂，仅供学习搜索引擎
    的工作原理。

概要
-----------------

- 爬虫：

    + 基于gevent
    + DNS本地缓存 dnsmasq
    + url存储 Mysql
    + url判重 md5

- 中文分词：

    + 基于词典，使用python dict存储

- 网页正文抽取：

    + 使用 lynx

- 倒排索引：

    + 使用 redis 2.6.0 bitmap
    + tf 使用 kyotocabinet存储

- 排序

    + 基于向量空间模型 TF-IDF

实现细节
-----------------

    + 待补充


协议
-----------------

    代码基于BSD协议发布

