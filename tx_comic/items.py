# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TxComicItem(scrapy.Item):
    image_urls = scrapy.Field()
    title_name = scrapy.Field()
    image = scrapy.Field()
    page_number = scrapy.Field()

