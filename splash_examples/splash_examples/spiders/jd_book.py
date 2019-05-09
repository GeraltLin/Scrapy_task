#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
from scrapy_splash import SplashRequest
from scrapy import Request
import scrapy
from scrapy.linkextractors import LinkExtractor


lua_script ='''
function main(splash)
    splash:go(splash.args.url)                                                                            
    splash:wait(3)
    splash:runjs("document.getElementById('footer-2017').scrollIntoView(true)")
    splash:wait(3)
    return splash:html()
    end
'''


class JDBookSpider(scrapy.Spider):
    name = "jd_book"
    allowed_domains = ["search.jd.com"]
    base_url = 'https://search.jd.com/search?keyword=neo4j&enc=utf-8&qrst=1&rt=1&stop=1&book=y&vt=2&wq=neo4j'

    def start_requests(self):

        yield Request(self.base_url,callback=self.parse_urls,dont_filter=True)


    def parse_urls(self, response):
        # 获取商品总数，计算出总页数

        # print(response.xpath('//span[@id = J_resCount]/text()').extract_first())
        #//*[@id="J_topPage"]/span/i
        # pageNum = int(response.xpath('//span[@class="fp-text]/span/i/text()').extract_first())
        # pageNum = total//60 + (1 if total%60 else 0)
        pageNum = int((response.xpath('//*[@id="J_topPage"]/span/i/text()')).extract_first())
        for i in range(pageNum):
            url = '%s&page=%s'%(self.base_url,2*i+1)
            yield SplashRequest(url,endpoint='execute',args={'lua_source':lua_script},cache_args=['lua_script'])


    def parse(self, response):
        for sel in response.css('ul.gl-warp.clearfix>li.gl-item'):
            yield {
                'name':sel.xpath('.//div[@class="p-name"]/a').xpath('string(.//em)').extract_first(),
                'price':sel.css('div.p-price i::text').extract_first()
            }