# coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import BookItem
import re


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    # 书籍的列表页面
    def parse(self, response):
        # 抽取书籍callback
        le = LinkExtractor(restrict_xpaths='//article/h3/a')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book)
        # 换页
        le = LinkExtractor(restrict_xpaths='//li[@class = "next"]')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_book(self, response):
        book = BookItem()
        sel = response.xpath('//div[@class="col-sm-6 product_main"]')
        book['name'] = sel.xpath('./h1/text()').extract_first()
        book['price'] = sel.xpath('./p[1]/text()').extract_first()
        book['review_rating'] = sel.xpath('./p[3]/@class').re_first('star-rating ([A-Za-z]+)')

        sel = response.xpath('//table[@class="table table-striped"]')
        table_data = sel.xpath('./tr/td/text()').extract()
        book['upc'] = table_data[0]
        book['stock'] = re.search('(\d+)', table_data[-2]).group()
        book['review_num'] = table_data[-1]
        yield book
