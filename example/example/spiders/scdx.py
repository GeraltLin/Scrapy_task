# coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import scrapy
from ..items import BookItem

import re

class SCDXSpider(scrapy.Spider):
    # 每个爬虫的唯一标识
    name = "scdx"

    # 定义爬虫起点，起点可以是多个，这里只有一个
    start_urls = ["http://jsuese.ijournals.cn/jsuese_cn/ch/mobile/m_article_status_query_data.aspx?file_no=201800001"]
    count = 201800002

    def parse(self, response):
        # 提取数据
        # 每一本书的位置在<article class="product_pod">
        text = response.xpath('/html/body/text()').extract_first()
        id = re.findall(r'\d+',text)[0]
        state = re.findall(r'稿件状态：.+?，', text)[0]
        yield {'id':id,'state':state}

        next_url = 'http://jsuese.ijournals.cn/jsuese_cn/ch/mobile/m_article_status_query_data.aspx?file_no=%s' % (
            self.count)
        if next_url:
            self.count = self.count +1
            yield scrapy.Request(next_url,callback=self.parse)

        #
        #     #<h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a>
        #
        #     name = book.xpath('./h3/a/@title').extract_first()
        #     #<div class="product_price"><p class="price_color">£17.46</p>
        #     price = book.xpath('./div[@class = "product_price"]/p/text()').extract_first()
        #     bookItem['name']=name
        #     bookItem['price']=price
        #     yield bookItem
        # # <li class="next"><a href="catalogue/page-2.html">next</a></li>
        #
        # le = LinkExtractor(restrict_xpaths='//li[@class = "next"]')
        # links = le.extract_links(response)
        # if links:
        #     next_url = links[0].url
        #     yield scrapy.Request(next_url, callback=self.parse)

        # next_url = response.xpath('//li[@class = "next"]/a/@href').extract_first()
        # if next_url:
        #     next_url = response.urljoin(next_url)
        #     yield scrapy.Request(next_url,callback=self.parse)

