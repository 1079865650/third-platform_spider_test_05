import scrapy
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, Float, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from scrapy import Request
from ..items import *
from ..db_utils import *
from ..parse_utils import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from pyquery import PyQuery as pq
from datetime import datetime


class SpiderConforamaSpider(scrapy.Spider):
    name = 'spider_conforama_asin'
    custom_settings = {
        'LOG_LEVEL': 'INFO',  # 日志级别
        'DOWNLOAD_DELAY': 1,  # 抓取延迟
        'CONCURRENT_REQUESTS': 20,  # 并发限制
        'DOWNLOAD_TIMEOUT': 60  # 请求超时
    }
    engine = get_engine()  # 连接数据库
    session = sessionmaker(bind=engine)
    sess = session()
    asintasks = sess.query(AsinTask, AsinTask.id, AsinTask.asin, AsinTask.href, AsinTask.plat, AsinTask.site, AsinTask.sp_tag) \
        .outerjoin(AsinAttr, and_(AsinTask.asin == AsinAttr.asin, AsinTask.site == AsinAttr.site)) \
        .filter(and_(AsinTask.status == None, AsinTask.plat == 'Conforama')).distinct()
    sess.close()

    headers_html = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-Encoding': "gzip, deflate, br",
        'accept-Language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache",
        'pragma': "no-cache",
        'sec-ch-ua': "\";Not A Brand\";v=\"99\", \"Chromium\";v=\"88\"",
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': "same-origin",
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    }
    def start_requests(self):
        count1 = 0
        for asin in self.asintasks:
            count1 += 1
            print('开始第'+str(count1)+'链接')
            yield Request(url=asin.href, callback=self.parse,
                          meta={'id': asin.id, 'asin': asin.asin, 'plat': asin.plat, 'site': asin.site, 'sp_tag': asin.sp_tag},
                          headers=self.headers_html)

    def parse(self, response):
        id = response.meta['id']
        plat = response.meta['plat']
        site = response.meta['site']
        asin = response.meta['asin']
        sp_tag = response.meta['sp_tag'] 
        doc = pq(response.text)

        item_attr = {}
        item_rank_list = []

        item_attr['plat'] = plat
        item_attr['asin'] = asin
        # item_rank 写入 sp_plat_site_asin_rank_conforama
        item_rank = item_attr.copy()
        item_rank['create_time'] = datetime.now()
        # 抓取prive,rating,reviews
        try:
            item_rank['price'] = extract_price(doc('div.currentPrice.typo-prix').html())
        except:
            item_rank['price'] = '0'
        item_rank['reviews'] = extract_number(
            doc('button#ratings-summary div.bv_numReviews_text').text())
        item_rank['rating'] = doc('button#ratings-summary div.bv_avgRating_component_container.notranslate').text()
        item_rank_list.append(item_rank)

        item_attr['seller'] = sp_tag
        item_attr['brand'] = sp_tag
        item_attr['site'] = site
        
        if str(sp_tag) == 'None':
            item_attr['seller'] = doc('.nameColorMp').text()
            item_attr['brand'] = item_attr['seller']
        
        href = doc('a[data-zoomproduct="true"]').attr('href')
        item_attr['imghref'] = href
        if 'discount à volonté' in doc('.fpCDAVLayerInfo.jsOverlay span').text():
            item_attr['sellertype'] = 'FBC'
        item_attr['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item_attr['update_time'] = item_attr['create_time']
        # print(item_attr, "========item_attr")
        # print(item_rank_list, "=======item_rank_list")

        yield {'data': item_attr, 'type': 'asin_attr'}
        yield {'data': {'id': id}, 'type': 'asin_task'}
        yield {'data': item_rank_list, 'type': 'asin_rank'}
        # yield {'data': item_rank_list, 'type': 'asin_rank_single'}

