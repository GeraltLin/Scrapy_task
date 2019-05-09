#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
from scrapy_splash import SplashRequest
import scrapy
from scrapy.linkextractors import LinkExtractor
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,args={'images':0,'timeout':3})

    def parse(self, response):
        for sel in response.xpath('//div[@class="quote"]'):
            qutoe = sel.xpath('./span[@class="text"]/text()').extract_first()
            author = sel.xpath('./span[@class="author"]/text()').extract_first()
            yield {'qutoe:':qutoe,'author':author}

        le = LinkExtractor(restrict_xpaths='//li[@class = "next"]')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield SplashRequest(next_url, args={'images':0,'timeout':3})