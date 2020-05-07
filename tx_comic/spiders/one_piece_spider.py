# -*- coding: utf-8 -*-
import scrapy
import os
import re
import execjs
from tx_comic.items import TxComicItem


class OnePieceSpiderSpider(scrapy.Spider):
    name = 'one_piece_spider'
    allowed_domains = ['pufei8.com']
    start_urls = ['http://www.pufei8.com/manhua/320/index.html']

    # def start_requests(self):
    #     yield scrapy.Request(url="http://www.pufei8.com/manhua/320/265337.html", callback=self.parse_imgurl_se,
    #                          meta={'index_name': "总356·继承人"})

    def parse(self, response):
        lis = response.xpath("//div[@id='play_0']/ul/li")
        print(len(lis))
        for li in lis:
            index_ulr = li.xpath(".//a/@href").get()
            index_name = li.xpath(".//a/text()").get()
            # print(index_name)
            # print(index_ulr)
            yield scrapy.Request(response.urljoin(index_ulr), callback=self.parse_imgurl_se,
                                 meta={'index_name': index_name})

    # def parse_imgurl(self, response):
    #     string = response.body.decode('utf-8', 'replace').replace("\r\n", "")
    #     script = re.findall(r'<script language="javascript" type="text/javascript">.*?</script>', string)
    #     fun = re.findall(r'function.*?};', script[0])
    #     packed = re.findall(r'packed=".*?"', script[0])
    #     # print(fun[0])
    #     # print(packed[0].split('"')[1])
    #
    #     fun = execjs.compile(fun[0])
    #     r = fun.call('base64decode', packed[0].split('"')[1])
    #     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img_url.js')
    #     # print(path)
    #     with open(path, 'r', encoding='utf-8') as fp:
    #         eval_fun = fp.read()
    #         loader = execjs.compile(eval_fun)
    #         page_number = loader.call('page_number', r)
    #         for page in range(page_number):
    #             number = page + 1
    #             index_img_url = response.urljoin(response.meta['index_url'] + "?page=" + str(number))
    #             yield scrapy.Request(index_img_url, callback=self.parse_imgurl_se,
    #                                  meta={'index_name': response.meta['index_name'], 'page_number': number,
    #                                      'pages_number':page_number})
        # print(string)

    def parse_imgurl_se(self, response):
        string = response.body.decode('utf-8', 'replace').replace("\r\n", "")
        script = re.findall(r'<script language="javascript" type="text/javascript">.*?</script>', string)
        fun = re.findall(r'function.*?};', script[0])
        packed = re.findall(r'packed=".*?"', script[0])
        # print(fun[0])
        # print(packed[0].split('"')[1])

        fun = execjs.compile(fun[0])
        r = fun.call('base64decode', packed[0].split('"')[1])
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img_url.js')
        # print(path)
        with open(path, 'r', encoding='utf-8') as fp:
            eval_fun = fp.read()
            loader = execjs.compile(eval_fun)
            img_url = loader.call('img_url', r)
            urls = re.findall('images/.*?jpg/0' , img_url)
            for i in range(len(urls)):
                urls[i] = "http://res.img.fffimage.com/"+urls[i]
            print(urls)
            item = TxComicItem(image_urls = urls , title_name=response.meta['index_name'])
            yield item


            # page_number = loader.call('page_number', r)
            # img_url = "http://res.img.fffimage.com/" + img_url
            # self.img_urls.append(img_url)
            # print(img_url)
            # if len(self.img_urls) >= response.meta['pages_number']:
            #     item = TxComicItem(image_urls= self.img_urls, title_name=response.meta['index_name'],
            #                        page_number=response.meta['page_number'])
            #     yield item
