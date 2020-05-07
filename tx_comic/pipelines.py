# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline
from tx_comic import settings
import os


class TxComicPipeline(object):
    def __init__(self):
        self.fp = open('img_urls.json', 'wb')
        self.expoter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def open_spider(self, spider):
        print("爬虫开始了")

    def process_item(self, item, spider):
        self.expoter.export_item(item)
        return item
    def close_spider(self, spider):
        print("爬虫结束啦")
        self.fp.close()



class TxComicDownloaderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(TxComicDownloaderPipeline, self).get_media_requests(item , info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs


    def file_path(self, request, response=None, info=None):
        title_name = request.item.get('title_name')
        url = request.url
        # print("request.url")
        # print(url)
        img_urls = request.item.get('image_urls')
        page_num = img_urls.index(url)
        img_name = str(page_num) + ".jpg"
        print(img_name)
        # print(page_num)
        imgs_store = settings.IMAGES_STORE
        title_path = os.path.join(imgs_store , title_name)
        if not os.path.exists(title_path):
            os.mkdir(title_path)

        img_path = os.path.join(title_path, img_name)
        print(img_path)
        return img_path

