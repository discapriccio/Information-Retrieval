# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()  #详情页面
    nameAndAuthor = scrapy.Field()  #题名/责任者
    press = scrapy.Field()  #出版发行项
    ISBNAndPrice = scrapy.Field()  #ISBN及定价
    subject = scrapy.Field()  #学科主题
    relRef1 = scrapy.Field()  # 相关链接1
    relRef2 = scrapy.Field()  # 相关链接2
    pass
