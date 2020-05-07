# -*- coding: utf-8 -*-
import js2py
import scrapy
import os
import re
import execjs
from tx_comic.items import TxComicItem


class KanikeCartoonSpiderSpider(scrapy.Spider):
    name = 'kanike_cartoon_spider'
    allowed_domains = ['manhuadui.com']
    start_urls = ['https://www.manhuadui.com/manhua/dongjingshishigui/']

    # def start_requests(self):
    #     yield scrapy.Request(url="https://www.manhuadui.com/manhua/dongjingshishigui/175289.html" , callback=self.parse_imgurl_se)

    def parse(self, response):
        lis = response.xpath("//div[@class='zj_list_con autoHeight']/ul/li")
        print(len(lis))
        for li in lis:
            index_ulr = li.xpath(".//a/@href").get()
            index_name = li.xpath(".//a/@title").get()
            # print(index_name)
            # print(index_ulr)
            url_num = re.findall(r'\d.*?\.' , index_ulr)[0].replace("." , "")
            # print(url_num)
            yield scrapy.Request(response.urljoin(index_ulr), callback=self.parse_imgurl_se,
                                 meta={"index_url": response.urljoin(index_ulr), "url_num": url_num , "index_name":index_name})

    def parse_imgurl_se(self, response):
        string = response.body.decode('utf-8', 'replace').replace("\r\n", "")
        # print(string)
        script = re.findall(r'chapterImages = ".*?";', string)
        # print(script)
        chapterImages_yuan = re.findall(r'".*?"', script[0])
        chapterImages = chapterImages_yuan[0].replace('"', "")
        print(chapterImages)
        with open("tx_comic/spiders/kanike_decode.js", 'r', encoding='utf-8') as fp:
            decode_fun = fp.read()
            loader = js2py.EvalJs()
            loader.execute(decode_fun)
            chapterImage_urls_str = loader.decrypt20180904(chapterImages)
            chapterImage_urls = chapterImage_urls_str.split('","')
            chapterImage_urls[0] = re.findall(r'\w.*?.jpg' , chapterImage_urls[0])[0]
            chapterImage_urls[-1] = re.findall(r'.*?.jpg' , chapterImage_urls[-1])[0]
            if "https" not in chapterImage_urls[0]:
                for i in range(len(chapterImage_urls)):
                    chapterImage_urls[i] = "https://img01.eshanyao.com/images/comic/32/"+response.meta['url_num']+"/"+chapterImage_urls[i]
            # print(chapterImage_urls)
            if "https" in chapterImage_urls[0]:
                for i in range(len(chapterImage_urls)):
                    chapterImage_urls[i] = chapterImage_urls[i].replace("\\" , "")
            item = TxComicItem(image_urls = chapterImage_urls , title_name=response.meta['index_name'])
            yield item

            # page_number = loader.call('page_number', r)
            # img_url = "http://res.img.fffimage.com/" + img_url
            # self.img_urls.append(img_url)
            # print(img_url)
            # if len(self.img_urls) >= response.meta['pages_number']:
            #     item = TxComicItem(image_urls= self.img_urls, title_name=response.meta['index_name'],
            #                        page_number=response.meta['page_number'])
            #     yield item
