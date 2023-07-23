import scrapy
from bs4 import BeautifulSoup


class FirstScrapy(scrapy.Spider):
    # 爬虫名 必须唯一
    name = "first"
    # 允许爬取的域名，如果不在这些域名内的链接将被过滤掉。start_urls里的域名不会被过滤。
    #allowed_domains = [""]
    start_urls = [
        "https://www.bmlink.com/"
    ]

    # parse方法作为回调函数(callback)赋值给了Request。request的响应（response）会赋值给该方法
    def parse(self, response):

        lis = response.xpath("//div[@class='hot_product']/ul/li").extract()
        for li in lis:
            print(li)



