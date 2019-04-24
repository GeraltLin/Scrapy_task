#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""

import scrapy
from scrapy.http import Request,FormRequest

class Examplelogin(scrapy.Spider):
    name = "examplelogin"
    allowed_domains = ["example.webscraping.com"]
    star_urls = ["http://example.webscraping.com/places/default/user/profile?_next=/places/default/index"]

    def parse(self, response):
        # print('response',response.xpath())
        keys = response.xpath('//table//label/text()').extract()
        # print('keys',response.xpath('//table//label/text()')).extract()

        values = response.xpath('//table//td[@class = "w2p_fw"]/text()').extract()

        print('values',values)

        yield dict(zip(keys,values))


    login_url = "http://example.webscraping.com/places/default/user/login"

    def start_requests(self):
        yield Request(self.login_url,callback=self.login)

    def login(self,response):
        fd = {'email':'liushuo@webscraping.com','password':'12345678'}
        yield FormRequest.from_response(response,formdata=fd,callback = self.parse_login)

    def parse_login(self,response):
        if 'Welcome Liu' in response.text:
            # yield from super.start_requests()
            yield Request(self.star_urls[0],callback=self.parse)