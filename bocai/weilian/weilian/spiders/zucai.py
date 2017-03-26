# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup as me
from datetime import datetime
from weilian.items import WeilianItem



class ZucaiSpider(scrapy.Spider):
    name = "zucai"
    allowed_domains = ["http://sports.williamhill.com"]


    def start_requests(self):
        uri = "http://sports.williamhill.com/bet/en-gb/betting/y/5/et/Football.html"
        resp = requests.get(uri)
        soup = me(resp.content)
        ul = soup.find('ul', class_='matrixB')
        li_list = ul.select('li > a')
        uri_list = [i['href'] for i in li_list]
        for i in uri_list:
            yield scrapy.Request(i,callback=self.parse1)

    def parse1(self,response):
            soup = me(response.body)
            item = WeilianItem()
            live = soup.find_all('tr', class_='rowLive')
            if live:
                for i in live:
                    item['kaisaishijian'] = 'live'
                    item['bisaishuangfang'] = i.find_all('td')[2].find('span').get_text()
                    item['zhupei'] = i.find_all('td')[4].find('div',class_='eventprice').get_text().strip()
                    item['pingpei'] = i.find_all('td')[5].find('div',class_='eventprice').get_text().strip()
                    item['kepei'] = i.find_all('td')[6].find('div',class_='eventprice').get_text().strip()
                    item['suoshuliansai'] = soup.find('ul',id='breadcrumb').find_all('li')[3].get_text()
                    item['zhuaqushijian'] = datetime.now()
                    item['laiyuanzhandian'] = 'weilianxier'
                    yield item
            else:
                pass
            odd = soup.find_all('tr',class_='rowOdd')
            if odd:
                for j in odd:
                    if j.find_all('td')[0].find('span'):
                        item['kaisaishijian'] = str(j.find_all('td')[0].find('span').get_text()) + str(j.find_all('td')[1].find('span').get_text())
                    else:
                        item['kaisaishijian'] = j.find_all('td')[1].find('a').get_text()
                    item['bisaishuangfang'] = j.find_all('td')[2].find('span').get_text()
                    item['zhupei'] = j.find_all('td')[4].find('div',class_='eventprice').get_text().strip()
                    item['pingpei'] = j.find_all('td')[5].find('div',class_='eventprice').get_text().strip()
                    item['kepei'] = j.find_all('td')[6].find('div',class_='eventprice').get_text().strip()
                    item['suoshuliansai'] = soup.find('ul', id='breadcrumb').find_all('li')[3].get_text()
                    item['zhuaqushijian'] = datetime.now()
                    item['laiyuanzhandian'] = 'weilianxier'
                    yield item
            else:
                pass




