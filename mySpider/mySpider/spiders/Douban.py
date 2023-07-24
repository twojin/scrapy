import scrapy
from ..items import DoubanBookItem

class DoubanScrapy(scrapy.Spider):
    # 爬虫名 必须唯一
    name = "douban"
    # 允许爬取的域名，如果不在这些域名内的链接将被过滤掉。start_urls里的域名不会被过滤。
    # allowed_domains = [""]
    start_urls = [
        "https://read.douban.com/category/100?sort=hot&page=1"
    ]

    # parse方法作为回调函数(callback)赋值给了Request。request的响应（response）会赋值给该方法
    def parse(self, response):
        bookList = response.xpath('//div[@class="section-works"]/ul/li[@class="works-item "]')
        for book in bookList:

            # 题目
            item = DoubanBookItem()
            item['title'] = book.xpath(".//span[@class='title-text']/span/text()").extract_first()

            # 作者和翻译员
            authorList = book.xpath(".//div[@class='author']/a")
            if len(authorList) > 1:
                item['author'] = authorList[0].xpath("./span/span/text()").extract_first()
                item['introduction'] = authorList[1].xpath("./span/span/text()").extract_first()

            else:
                item['author'] = authorList[0].xpath("./span/span/text()").extract_first()

            print(item)












