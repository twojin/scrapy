# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


# class MyspiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class DoubanBookItem(Item):

    title = Field()
    author = Field()
    translator = Field()
    introduction = Field()
    kind = Field()
    wordCount = Field()
    originalPrice = Field()
    discountPrice = Field()
