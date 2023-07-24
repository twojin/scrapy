import scrapy


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
        bookList = response.xpath('//*[@id="react-root"]/div/section[2]/div/ul/li').extract()
        for book in bookList:
            print(book)

