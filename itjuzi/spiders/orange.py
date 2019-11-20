# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError


from itjuzi.items import ItjuziItem
class OrangeSpider(scrapy.Spider):
    name = 'orange'
    allowed_domains = ['www.itjuzi.com']
    page = 1
    url = "https://www.itjuzi.com/api/closure?com_prov=&sort=&keyword=&cat_id=&page="
    start_urls = [url+str(page),]

    def parse(self, response):
        data = json.loads(response.text)
        infos = jsonpath.jsonpath(data,"$..info")[0]
        for info in infos:
            item = ItjuziItem()

            # 公司id
            item['com_id'] = jsonpath.jsonpath(info,'$..com_id')[0]
            # 公司名称
            item['com_name'] = jsonpath.jsonpath(info,'$..com_name')[0]
            # 关闭时间
            item['com_change_close_date'] = jsonpath.jsonpath(info,'$..com_change_close_date')[0]
            # 公司简介
            item['com_des'] = jsonpath.jsonpath(info,'$..com_des')[0]
            # 行业
            item['cat_name'] = jsonpath.jsonpath(info,'$..cat_name')[0]
            # 地点
            item['com_prov'] = jsonpath.jsonpath(info,'$..com_prov')[0]
            # 获投状态
            item['com_fund_status_name'] = jsonpath.jsonpath(info,'$..com_fund_status_name')[0]
            # 成立时间
            item['born'] = jsonpath.jsonpath(info,'$..born')[0]
            # 存活天数
            item['live_time'] = jsonpath.jsonpath(info,'$..live_time')[0]
            # 团队
            item['com_team'] = jsonpath.jsonpath(info,'$..com_team..name')
            # 行业标签
            item['com_tag'] = ",".join(jsonpath.jsonpath(info,'$..com_tag..tag_name'))
            # 死亡原因
            item['closure_type'] = jsonpath.jsonpath(info,'$..closure_type..name')
            yield item
        self.page += 1
        yield scrapy.Request(self.url+str(self.page),callback=self.parse,errback=self.errback_httpbin)

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        # if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        # elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        # elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)