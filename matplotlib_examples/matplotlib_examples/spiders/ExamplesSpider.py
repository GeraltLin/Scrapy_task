#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import MatplotlibExamplesItem

class ExamplesSpider(scrapy.Spider):
    name = "examples"
    allowed_domains = ["matplotlib.org"]
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//li[@class="toctree-l2"]')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url,callback=self.parse_example)

    def parse_example(self,response):
        py_url = response.xpath('//a[@class = "reference external"]/@href').extract_first()
        py_url = response.urljoin(py_url)
        example = MatplotlibExamplesItem()
        example['file_urls'] = [py_url]
        return example
