# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class ItjuziPipeline(object):
    def process_item(self, item, spider):

        if item['closure_type'] != False:
            item['closure_type'] = ",".join(item['closure_type'])
        else:
            item['closure_type'] = " "
        if item['com_team'] != False:
            item['com_team'] = ",".join(item['com_team'])
        else:
            item['com_team'] = " "


        return item


class MysqlPipeline(object):
    def __init__(self, host, user, password, database,port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self,spider):
        """
        当Spider开启时，这个方法被调用
        :param spider: Spider 的实例
        :return:
        """
        self.conn = pymysql.connect(
            host =self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """
        当Spider关闭时，这个方法被调用
        :param spider:
        :return:
        """
        self.cursor.close()
        self.conn.close()

    def process_item(self,item,spider):
        # data = dict(item)
        # keys = ','.join(data.keys())
        # values = ','.join(['%s'*len(data)])

        sql = "insert into death_com_new (com_id, com_name, com_change_close_date, com_des, cat_name, com_prov, com_fund_status_name, born, live_time, com_team, com_tag, closure_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        self.cursor.execute(sql, [item['com_id'],item['com_name'],item['com_change_close_date'],item['com_des'],item['cat_name'],item['com_prov'],item['com_fund_status_name'],item['born'],item['live_time'],item['com_team'],item['com_tag'],item['closure_type']])
        self.conn.commit()
        return item
