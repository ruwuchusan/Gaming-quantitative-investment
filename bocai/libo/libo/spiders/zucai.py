# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from libo.items import LiboItem
from fractions import Fraction


class ZucaiSpider(scrapy.Spider):
    name = "zucai"
    allowed_domains = ["https://sports.ladbrokes.com/"]
    # start_urls = ('https://sports.ladbrokes.com/en-gb/events/sport/110000006/leagues')


    def start_requests(self):
        yield scrapy.Request('https://sports.ladbrokes.com/en-gb/events/sport/110000006/leagues',callback=self.parse)

    def parse(self, response):
        item = LiboItem()
        dict = json.loads(response.body)
        for i in dict['eventGroups']:
            if i.has_key('list'):
                for j in i['list']:
                    try:
                        time_local = time.localtime(float(j['event']['startTime'])/1000)
                        item['kaisaishijian'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                        item['bisaishuangfang'] = j['event']['nameTranslations']['value']
                        # item['zhudui'] = j['event']['nameTranslations']['value'].split(u'<b>v</b>')[0]
                        # item['kedui'] = j['event']['nameTranslations']['value'].split(u'<b>v</b>')[1]
                        item['suoshuliansai'] = i['title']
                        item['zhupei'] = float(Fraction(j['event']['mainMarket']['selections'][0]['prices'][0]['fractionalOdds']))+1
                        item['pingpei'] = float(Fraction(j['event']['mainMarket']['selections'][1]['prices'][0]['fractionalOdds']))+1
                        item['kepei'] = float(Fraction(j['event']['mainMarket']['selections'][2]['prices'][0]['fractionalOdds']))+1
                        item['zhuaqushijian'] = datetime.now()
                        item['laiyuanzhandian'] = 'ladbrokes'
                        yield item
                    except:
                        pass
            else:
                pass




