# baike_scrapy
使用scrapy爬取百度百科
包括词、词摘要、基本信息、摘要链接、内容等保存到baike/spaiders目录下的baike.json文件中


1.需要安装myslq数据库 然后运行 baike/mysql/test.py文件创建数据库表格

2.进入命令行运行 scrapy crawl baike 即可

3.所有的相关信息保存到baike/spiders/baike.log中，为后续的使用，控制台不在显示运行信息

4.输出数据保存在baike/spiders/baike.json下，每行一个词条为,例如多义词信息如下： 
{"title": "百度百科：多义词", "url": "https://baike.baidu.com/item/百度百科：多义词", "summary": "\n百度百科里，当同一个词条名可指代含义概念不同的事物时，这个词条称为多义词。如词条“苹果”，既可以代表一种水果，也可以指代苹果公司，因此“苹果”是一个多义词。\n", "summarylinks": [["百度百科"], ["/item/百度百科"]], "basicinfo": [[], []], "content": "", "contentlinks": [["义项"], ["/item/义项"]]}

5.在baike/mysql/json_test.py有队生成baike.json的相关调试
