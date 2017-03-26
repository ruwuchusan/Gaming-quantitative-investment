# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from bs4 import BeautifulSoup as me
from unibet.items import UnibetItem
from datetime import datetime
from fractions import Fraction


class ZucaiSpider(scrapy.Spider):
    name = "zucai"
    allowed_domains = ["https://www.unibet.co.uk/"]


    def start_requests(self):
        # 获取所有联赛
        uri = 'https://e4-api.kambi.com/offering/api/v2/ubuk/group.json?lang=en_GB&market=GB&client_id=2&channel_id=1&ncid=1489038631842'
        a = requests.get(uri).content
        b = json.loads(a)
        c = b['group']['groups'][0]
        list = []
        for i in c['groups']:
            try:
                list.append({i['name']: [j['name'] for j in i['groups']]})
            except:
                pass

        #拼接每个联赛的URI
        list_competition = []
        uri_content = 'https://e4-api.kambi.com/offering/api/v3/ubuk/listView/football/tunisia/ligue_1.json?lang=en_GB&market=GB&client_id=2&channel_id=1&ncid=1489042133369&categoryGroup=COMBINED&displayDefault=true'
        for j in list:
            for z in j.values()[0]:
                yield scrapy.Request(uri_content.replace('tunisia',j.keys()[0].lower()).replace('ligue_1',z.lower().replace(' ','_')),callback=self.parse1)


    def parse1(self,response):
        item = UnibetItem()
        try:
            dict = json.loads(response.body)
            for i in dict['events']:
                # item['bisaishuangfang'] = i['event']['englishName']
                item['zhudui'] = i['event']['englishName'].split('-')[0].strip()
                item['kedui'] = i['event']['englishName'].split('-')[1].strip()
                item['kaisaishijian'] = i['betOffers'][0]['closed']
                item['zhupei'] = float(Fraction(i['betOffers'][0]['outcomes'][0]['oddsFractional']))+1
                item['pingpei'] = float(Fraction(i['betOffers'][0]['outcomes'][1]['oddsFractional']))+1
                item['kepei'] = float(Fraction(i['betOffers'][0]['outcomes'][2]['oddsFractional']))+1
                item['suoshuliansai']  = str(i['event']['path'][1]['englishName']) + "+" + str(i['event']['path'][2]['englishName'])
                item['zhuaqushijian'] = datetime.now()
                item['laiyuanzhandian'] = 'unibet'
                yield item
        except:
            pass






