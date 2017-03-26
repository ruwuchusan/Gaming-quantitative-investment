# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup as me
from interwetten.items import InterwettenItem
from datetime import datetime

class ZucaiSpider(scrapy.Spider):
    name = "zucai"
    allowed_domains = ["https://www.interwetten.com/"]


    def start_requests(self):
        uri = 'https://www.interwetten.com/en/sportsbook/o/10/football'
        soup = me(requests.get(uri).content)
        table = soup.find('table', id='TBL_Content_Leagues')
        tr_list = table.children
        uri_fragment_list = []
        for i in tr_list:
            if i.find('a') == -1:
                pass
            else:
                uri_fragment_list.append(i.find('a'))

        for j in uri_fragment_list:
            full_uri = 'https://www.interwetten.com'+j['href']
            suoshubisai = j['href'].split('/')[5]
            yield scrapy.Request(full_uri,callback=self.parse1,meta={'suoshubisai':suoshubisai})


    def parse1(self, response):
        soup  = me(response.body)
        div = soup.find('div', class_='bets shadow')
        table = div.find('table')
        tr_list = table.children
        list = []
        for i in tr_list:
            if i == '\n':
                pass
            else:
                list.append(i)
        useful_list = list[2:]

        #获取标签为playtime的tr的index
        playtime_index = []
        for i in useful_list:
            if i.find('td'):
                if i.find('td')['class'] == ['playtime']:
                    playtime_index.append(useful_list.index(i))
                else:
                    pass
            else:
                pass

        #以时间分组，每场比赛状况
        content_list = []
        for i in range(len(playtime_index)):
            if i < len(playtime_index) - 1:
                content_list.append(useful_list[playtime_index[i]:playtime_index[i + 1]])
            else:
                content_list.append(useful_list[playtime_index[i]:])
        #抽取内容
        item = InterwettenItem()
        for i in content_list:
            for j in i:
                if j.find('td')['class'] == ['playtime']:
                    pass
                else:
                    item['kaisaishijian'] = i[0].get_text().strip() + "+" + j.find('td', class_='date dtstart').get_text().strip()
                    item['zhudui'] = j.find('td',class_='bets').find('p',itemprop='homeTeam').find('span',itemprop='name').get_text()
                    item['kedui'] = j.find('td', class_='bets').find('p',itemprop='awayTeam').find('span',itemprop='name').get_text()
                    item['zhupei'] = j.find('td', class_='bets').find('p',itemprop='homeTeam').find( 'strong').get_text().replace(',','.')
                    item['pingpei'] = j.find('td', class_='bets').find_all('p')[1].find( 'strong').get_text().replace(',','.')
                    item['kepei'] = j.find('td', class_='bets').find('p', itemprop='awayTeam').find( 'strong').get_text().replace(',','.')
                    item['suoshuliansai'] = response.meta['suoshubisai']
                    item['zhuaqushijian'] = datetime.now()
                    item['laiyuanzhandian'] = 'interwetten'
                    yield item









