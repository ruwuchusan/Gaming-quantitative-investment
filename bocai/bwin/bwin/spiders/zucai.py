# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as me
from bwin.items import BwinItem
from datetime import datetime


class ZucaiSpider(scrapy.Spider):
    name = "zucai"
    allowed_domains = ["www.bwin1828.com"]
    start_urls = (
        'https://www.bwin1828.com/en/sport/football/',
    )

    def parse(self, response):
        soup = me(response.body)
        section_list = soup.find_all('section',class_='coupon-homepage__group index_group')
        for i in section_list:
            for j in i.find_all('p',class_='coupon-homepage__group-item inner_meetings other')+i.find_all('p',class_='coupon-homepage__group-item inner_meetings last'):
                yield scrapy.Request('https://www.bwin1828.com'+str(j.find('a')['href']),callback=self.parse1,meta={"data":j.find('a')['href']})


    def parse1(self,response):
        soup = me(response.body)
        item = BwinItem()
        date_list = soup.find_all('table',class_='has_group_date')
        for i in date_list:
            table = i.find('table')
            date = i.select('tbody > tr > td[class="group_date"]')[0].get_text()
            for j in table.find_all('tr',class_='body'):
                item['kaisaishijian'] = str(j.find('span',class_='localized-time').get_text())+str(date)
                item['bisaishuangfang'] = j.find('a',class_='title-wrapper').get_text()
                item['zhupei'] = j.find_all('td',class_='outcome_td outcome-bet-button-wrapper')[0]['data-sort']
                item['pingpei'] = j.find_all('td', class_='outcome_td outcome-bet-button-wrapper')[1]['data-sort']
                item['kepei'] = j.find_all('td', class_='outcome_td outcome-bet-button-wrapper')[2]['data-sort']
                item['suoshuliansai'] = response.meta['data'].split('en/sport/football/')[1].split('/coupons')[0]
                item['zhuaqushijian'] = datetime.now()
                item['laiyuanzhandian'] = 'bwin'
                yield item





