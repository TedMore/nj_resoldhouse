# -*- coding: utf-8 -*-
import scrapy
from nj_resoldhouse.items import NjResoldhouseItem
import re

class LjResoldhouseSpider(scrapy.Spider):
    name = 'lj_resoldhouse'
#     allowed_domains = ['nj.lianjia.com/ershoufang']
    start_urls = ['http://nj.lianjia.com/ershoufang/']

    def parse(self, response):
        clears = response.css('.sellListContent li')
        for c in clears:
            item = NjResoldhouseItem()
            try:
                house = c.css('.houseInfo a::text').extract_first()
                house_text = c.css('.houseInfo::text').extract_first()
                house_info_list = [e for e in re.split('\|', house_text) if len(e) > 1]
                house_room = house_info_list[0].strip()
                house_area = ''.join(re.findall(r'[\d+\.]', house_info_list[1]))
                total_price = c.css('.totalPrice span::text').extract_first()
                unit_price = c.css('.unitPrice span::text').extract_first()
                unit_price = re.findall('\d+', unit_price)[0]
                
                item['house'] = house
                item['house_room'] = house_room
                item['house_area'] = float(house_area)
                item['total_price'] = float(total_price)
                item['unit_price'] = float(unit_price)
                
                yield item
            except Exception as e:
                print e, house_info_list     
        
        page_info = response.css('div[class="page-box fr"]').css('div::attr(page-data)').extract_first()
        page_list = re.findall('\d+', page_info)
        next_page = 'pg' + str(int(page_list[1]) + 1)
        url = self.start_urls[0] + next_page
        if url is not None:
            yield scrapy.Request(response.urljoin(url))
