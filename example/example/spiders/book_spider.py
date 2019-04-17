# coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import scrapy
from ..items import BookItem
from scrapy.linkextractors import LinkExtractor

class BookSpider(scrapy.Spider):
    # 每个爬虫的唯一标识
    name = "books"

    # 定义爬虫起点，起点可以是多个，这里只有一个
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        # 提取数据
        # 每一本书的位置在<article class="product_pod">
        for book in response.xpath('//article'):
            bookItem=BookItem()

            #<h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a>

            name = book.xpath('./h3/a/@title').extract_first()
            #<div class="product_price"><p class="price_color">£17.46</p>
            price = book.xpath('./div[@class = "product_price"]/p/text()').extract_first()
            bookItem['name']=name
            bookItem['price']=price
            yield bookItem
        # <li class="next"><a href="catalogue/page-2.html">next</a></li>

        le = LinkExtractor(restrict_xpaths='//li[@class = "next"]')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

        # next_url = response.xpath('//li[@class = "next"]/a/@href').extract_first()
        # if next_url:
        #     next_url = response.urljoin(next_url)
        #     yield scrapy.Request(next_url,callback=self.parse)

