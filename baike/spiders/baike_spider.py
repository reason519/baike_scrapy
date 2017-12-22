from urllib.parse import unquote

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.cmdline import execute
import re
import logging

from ..items import BaikeItem
from ..mysql_conn import Mysql


class MySpider(CrawlSpider):
    name = 'baike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com']
    #start_urls=['https://baike.baidu.com/item/昆曲/216928?secondId=121630&mediaId=mda-gmrx0rhf23gtx296']


    #下面的start_urls用于测试subview与view
    #start_urls=['http://baike.baidu.com/fenlei/%E6%BC%94%E5%87%BA']

    db=Mysql()
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('baike.baidu.com', ), deny=('https?://baike.baidu.com/item','https?://baike.baidu.com/subview',
                                               'https?://baike.baidu.com/view','https://baike.baidu.com/tashuo','https?://baike.baidu.com/pic',
                                               'https://baike.baidu.com/history','https://baike.baidu.com/historypic',
                                               'http://baike.baidu.com/mall','https?://baike.baidu.com/albums?',
                                                'https?://baike.baidu.com/article','https://baike.baidu.com/difangzhi'
                                               'http://baike.baidu.com/campus','https://baike.baidu.com/redirect',
                                                'https://baike.baidu.com/divideload'
                                               )),process_links='process_links',follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('https?://baike.baidu.com/subview',)), callback='parse_word',follow=True,process_links="proc_subview_links"),
        Rule(LinkExtractor(allow=('https?://baike.baidu.com/view',)), callback='parse_word',follow=True,process_links="proc_view_links"),
        Rule(LinkExtractor(allow=('https?://baike.baidu.com/item', )), callback='parse_word',follow=True,process_links="proc_item_links"),
    )

    #过滤掉已经访问过的请求
    def process_links(self,links):
        for link in links:
            try:
                self.db.insert_urlfilter(unquote(link.url))
            except:
                links.remove(link)
        return links

    def proc_item_links(self,links):
        for link in links:
            try:
                self.db.insert_itemfilter(re.split('[#]',unquote(link.url[link.url.find('/item/')+6:]))[0])
            except:
                links.remove(link)
        return links

    def proc_view_links(self,links):
        for link in links:
            try:
                self.db.insert_viewfilter(unquote(link.url))
            except:
                links.remove(link)
        return links

    def proc_subview_links(self,links):
        for link in links:
            try:
                self.db.insert_subviewfilter(unquote(link.url))
            except:
                links.remove(link)
        return links

    def parse_word(self,response):
        title = response.xpath("//dl[contains(@class,'lemmaWgt-lemmaTitle')]//h1/text()").extract()
        summary=response.xpath("//div[@class='lemma-summary']")
        polysemy = response.xpath("//div[contains(@class,'polysemant-list')]//li[@class='item']/span[@class='selected']/text()")
        unquote_url=unquote(response.url)
        basic_info_name = response.xpath("//div[contains(@class,'basic-info')]//dt")
        basic_info_val = response.xpath("//div[contains(@class,'basic-info')]//dd")
        chapter = response.xpath("//div[@class='para-title level-2']")
        item=BaikeItem()
        #判断该页面是否为词条页面 通过是否存在title和摘要判断  url例外https://baike.baidu.com/item/%E7%9B%9B%E5%AE%A3%E6%80%80?force=1
        if len(title)!=0 and len(summary)!=0:
            #判断是否存在同义词条
            if response.url.find('fromtitle')!=-1 and '同义词' in response.xpath("//span[@class='view-tip-panel']/a/text()").extract():
                syn_word=self.process_synonym_url(unquote_url)
                syn_from= syn_word[0].split('/item/')
                syn=syn_word[0]
                if len(syn_from) == 2:
                    syn=syn_from[1]
                else:
                    logging.log("同义词url出现问题："+unquote_url)

                if len(syn_word)==3:
                    #原始词的url
                    pre_url='https://baike.baidu.com/item/' + syn_word[1] + '/' + syn_word[2]
                    if syn_word[2]=='':
                        syn_word[2]=0
                    try:
                        if len(polysemy.extract()) == 0:
                            self.db.insert_wordinfo(pre_url,syn_word[1],int(syn_word[2]),synonym=syn)
                        else:
                            self.db.insert_wordinfo(pre_url,syn_word[1],int(syn_word[2]),polysemy.extract()[0],synonym=syn)
                    except Exception as e:
                        logging.error("错误："+str(e))
                        logging.warning("该同义词已添加到数据库："+unquote_url)
                    yield scrapy.Request(syn_word[0])
            else:
                #将该词条保存到数据库
                wordid=self.process_word_url(unquote_url)
                try:
                    if len(polysemy.extract())==0:
                        self.db.insert_wordinfo(unquote_url,title[0],wordid)
                    else:
                        self.db.insert_wordinfo(unquote_url,title[0],wordid,polysemy.extract()[0])
                        # 将该次的信息写入文件中

                    item['title'] = title[0]
                    item['wordid'] = wordid
                    item['url'] = unquote_url
                    if len(polysemy.extract()) is not 0:
                        item['polysemy'] = polysemy.extract()[0]
                    item['summary'] = "".join(summary.xpath('.//text()').extract())
                    summary_a = summary.xpath(
                        ".//a[starts-with(@href,'/item')]//text()").extract()
                    summary_a_href = [unquote(x) for x in summary.xpath(
                        ".//a[starts-with(@href,'/item')]/@href").extract()]
                    item['summarylinks'] = [summary_a, summary_a_href]
                    # 基本信息处理

                    basic_info_name_item = ["".join(x.xpath(".//text()").extract()).strip() for x in
                                            basic_info_name]
                    basic_info_value_item = ["".join(x.xpath(".//text()").extract()).strip() for x in
                                             basic_info_val]
                    item['basicinfo'] = [basic_info_name_item, basic_info_value_item]

                    # 词的内容提取，只包含二级标题，忽略三级标题
                    content = ''
                    content_a = []
                    content_href = []
                    for ind, ch in enumerate(chapter, start=1):
                        # print(''.join(ch.xpath('./h2/text()').extract()).strip())
                        content_para = ch.xpath("./following-sibling::div[@class='para'][count(preceding-sibling::"
                                                "div[@class='para-title level-2'])=%d]" % ind)
                        for con in content_para:
                            content += "".join((con.xpath('.//text()').extract())).strip()
                            content_a.extend(con.xpath(
                                ".//a[starts-with(@href,'/item')]//text()").extract())
                           #     ".//a[@href and not(contains(@class,'image-link')) and not(contains(@class,'edit-icon')) ]//text()").extract())
                            content_href.extend([unquote(x) for x in con.xpath(
                                ".//a[starts-with(@href,'/item')]/@href").extract()])
                    item['content'] = content
                    item['contentlinks'] = [content_a, content_href]
                    yield item
                except Exception as e:
                    logging.error("错误：" + str(e))
                    logging.warning("该词已添加到数据库：" + unquote_url)
        else:
            #对可能存在的意外进行日志记录
            logging.warning("非词条页，请确认： "+unquote_url)

    def process_word_url(self,url):
        wordid=re.findall('/\d*$', url.split('?')[0])
        if len(wordid)==0:
            wordid=0
        else:
            wordid=int(wordid[0][1:])
        return wordid

    def process_synonym_url(self,url):
        # if url.rfind('?')!=-1:
        #     url_list = url.split('?')
        #     id_s = url_list[1].rfind('fromid=') + 7
        #     id_e = url_list[1].rfind('#')
        #     if id_e == -1:
        #         id_e = len(url)
        #     word_s = url_list[1].find('fromtitle=') + 10
        #     word_e = url_list[1].find('&')
        #     return (url_list[0],url_list[1][word_s:word_e],url_list[1][id_s:id_e])
        # return -1
        if url.rfind('?') != -1:
            url_list = url.split('?')
            if 'fromtitle=' in url_list[1] and 'fromid=' in url_list[1]:
                wl=url_list[1].split('&')
                
                for w in wl:
                    if 'fromtitle=' in w:
                        title=w[w.find('fromtitle=') + 10:len(w)]
                    if 'fromid=' in w:
                        id_s = w.rfind('fromid=') + 7
                        id_e = w.rfind('#')
                        if id_e == -1:
                            id_e = len(w)
                        id=w[id_s:id_e]
                        
                return (url_list[0],title, id)
            else:
                return -1
        return -1


if __name__=='__main__':
    execute(['scrapy', 'crawl', 'baike'])
