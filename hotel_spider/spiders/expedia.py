# -*- coding: utf-8 -*-
import scrapy
import pymysql

from scrapy.http import Request
from scrapy_splash import SplashRequest

from hotel_spider import settings
from hotel_spider.items import ProductItem

class ExpediaSpider(scrapy.Spider):
    name = 'expedia'
    allowed_domains = ['expedia.cn', 'travelads.hlserve.com']

    def start_requests(self):
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        cursor = connect.cursor()
        cursor.execute('select country, city from cities')
        ret = cursor.fetchall()
        for r in ret[:3]:
            country_name = r[0]
            city_name = r[1]
            url = 'https://www.expedia.cn/Hotel-Search?destination=' + city_name
            request = SplashRequest(url=url, callback=self.parse,
                                    args={
                                        'wait': 5,
                                        'timeout': 20,
                                        'headers': {
                                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
                                        }
                                    })
            request.meta['city'] = city_name
            request.meta['country'] = country_name
            yield request

    def parse(self, response):
        for hotel in response.css('article.hotel.listing'):
            hotel_name = hotel.css('.hotelName::text').extract_first()
            hotel_url = hotel.css('a.flex-link::attr(href)').extract_first()
            request = SplashRequest(url=hotel_url, callback=self.parse_hotel_detail_page,
                                    args={
                                        'wait': 5,
                                        'timeout': 20,
                                        'headers': {
                                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
                                        }
                                    })
            meta = request.meta
            meta['country'] = response.meta['country']
            meta['city'] = response.meta['city']
            meta['hotel_name'] = hotel_name
            meta['hotel_url'] = hotel_url
            yield request

    def parse_hotel_detail_page(self, response):
        meta = response.meta
        source = 'expedia'
        country = meta['country']
        city = meta['city']
        hotel_name = meta['hotel_name']
        hotel_url = meta['hotel_url']

        for room in response.css('tbody.room'):
            room_name = room.css('td.room-info .room-basic-info .room-name::text').extract_first()
            for product in room.css('td.avg-rate'):
                product_price = product.css('.room-price .room-price-value::text').extract_first()
                if product_price:
                    product_price = product_price.replace('￥', '')
                    product_price = product_price.strip()

                item = ProductItem()
                item['source'] = source
                item['country'] = country
                item['city'] = city
                item['hotel_name'] = hotel_name
                item['hotel_url'] = hotel_url
                item['room_name'] = room_name
                item['product_name'] = 'expedia product'
                item['product_price'] = product_price
                yield item