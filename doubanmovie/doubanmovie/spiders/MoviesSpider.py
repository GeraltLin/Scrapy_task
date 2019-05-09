#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import scrapy
from scrapy import Request
import json
import re
import urllib
from scrapy.http import Request,FormRequest

from pprint import pprint
from ..items import DoubanmovieItem

class MoviesSpider(scrapy.Spider):
    BASE_URL = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=%s&page_start=%s'
    MOVIE_TAG = '冷门佳片'
    PAGE_LIMIT = 20
    page_start = 0
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"} #供登录模拟使用


    name = "movies"
    urls = [BASE_URL%(MOVIE_TAG,PAGE_LIMIT,page_start)]

    def start_requests(self):
        # return [Request(url=url,meta={"cookiejar":1},callback=self.parse)]#可以传递一个标示符来使用多个。如meta={'cookiejar': 1}这句，后面那个1就是标示符
        # return [Request(url='https://movie.douban.com', meta={'cookiejar': 1}, callback=self.post_login)]
        return [Request(self.urls[0],callback=self.parse)]



    def post_login(self, response):
        return FormRequest(
            url='https://accounts.douban.com/j/mobile/login/basic',
            method='POST',
            formdata={
                'ck': '',
                'name': '18883287013@163.com',
                'password': 'lwxqq220114',
                'remember': 'false',
                'ticket': ''
            },
            meta={'cookiejar': response.meta['cookiejar']},
            dont_filter=True,
            callback=self.get_content
        )


    def get_content(self, response):
        status = json.loads(response.body.decode('utf8'))['status']

        if status == 'failed':
            print("登录失败，请重试")
        else:
            print("登陆成功")
            yield Request(self.urls[0],callback=self.parse)


    def parse(self, response):

        infos = json.loads(response.body.decode('utf8'))
        for movie_infro in infos['subjects']:
            movieItem = {}
            movieItem['电影'] = movie_infro['title']
            yield Request(movie_infro['url'],callback=self.parse_movie,meta={'theItem':movieItem})

        if len(infos['subjects']) ==self.PAGE_LIMIT:
            self.page_start += self.PAGE_LIMIT
            url = self.BASE_URL % (self.MOVIE_TAG,self.PAGE_LIMIT,self.page_start)
            yield Request(url)

    def parse_movie(self,response):
        movieItem = response.meta['theItem']

        info = response.xpath('//div[@id="info"]').xpath('string(.)').extract_first()

        fields = [s.strip().replace(':','') for s in response.xpath('//div[@id="info"]//span[@class="pl"]/text()').extract()]

        values = [re.sub('\s+','',s.strip()) for s in re.split('\s*(?:%s):\s*'%'|'.join(fields),info)][1:]

        movieItem.update(dict(zip(fields,values)))

        yield movieItem
