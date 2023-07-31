# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql

from twisted.enterprise import adbapi


class MyspiderPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
    def __init__(self, host, database, port, user, password):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password

    @classmethod
    # 获取settings配置文件当中设置的MySQL各个参数
    def from_crawler(cls, crawler):
        s = cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            port=crawler.settings.get("MYSQL_PORT"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD")
        )
        # open_spider、process_item、close_spider为默认方法无需手动设置信号量
        return s;

    # 开启爬虫时连接MongoDB数据库
    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, database=self.database, user=self.user, password=self.password,
                                  port=self.port, charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ",".join(data.keys())  # 字段名
        values = ",".join(["%s"] * len(data))  # 值
        sql = "insert into %s (%s) values(%s)" % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

    # 关闭爬虫时断开MongoDB数据库连接
    def close_spider(self, spider):
        self.db.close()


class MysqlTwistedPipeline:
    def __init__(self, params: dict):
        self.db_connect_pool = None
        self.params = params

    @classmethod
    # 获取settings配置文件当中设置的MySQL各个参数
    def from_crawler(cls, crawler):
        params = dict(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            port=crawler.settings.get("MYSQL_PORT"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )

        s = cls(
            params
        )
        # open_spider、process_item、close_spider为默认方法无需手动设置信号量
        return s;

    # 开启爬虫时连接MongoDB数据库
    def open_spider(self, spider):
        self.db_connect_pool = adbapi.ConnectionPool('pymysql', **self.params)

    def process_item(self, item, spider):
        result = self.db_connect_pool.runInteraction(self.insert, item)
        # 给result绑定一个回调函数，用于监听错误信息
        result.addErrback(self.error)

    def insert(self, cursor, item):
        data = dict(item)
        keys = ",".join(data.keys())  # 字段名
        values = ",".join(["%s"] * len(data))  # 值
        sql = "insert into %s (%s) values(%s)" % (item.table, keys, values)
        cursor.execute(sql, tuple(data.values()))

    def error(self, reason):
        print('--------', reason)

    # 关闭爬虫时断开MongoDB数据库连接
    def close_spider(self, spider):
        self.db_connect_pool.close()
