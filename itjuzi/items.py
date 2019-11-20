# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # 公司id
    com_id = scrapy.Field()
    # 公司名称
    com_name = scrapy.Field()
    # 关闭时间
    com_change_close_date = scrapy.Field()
    # 公司简介
    com_des = scrapy.Field()
    # 行业
    cat_name = scrapy.Field()
    # 地点
    com_prov = scrapy.Field()
    # 获投状态
    com_fund_status_name = scrapy.Field()
    # 成立时间
    born = scrapy.Field()
    # 存活天数
    live_time = scrapy.Field()
    # 团队
    com_team = scrapy.Field()
    # 行业标签
    com_tag = scrapy.Field()
    # 死亡原因
    closure_type = scrapy.Field()
