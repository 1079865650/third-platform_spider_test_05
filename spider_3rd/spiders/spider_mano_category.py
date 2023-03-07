import sys
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


class SpiderManoSpider(scrapy.Spider):
    name = 'spider_mano_category'

    custom_settings = {  # 62  18 18 18  8
        'LOG_LEVEL': 'INFO',  # 日志级别
        'DOWNLOAD_DELAY': 5,  # 抓取延迟
        'CONCURRENT_REQUESTS': 20,  # 并发限制
        'DOWNLOAD_TIMEOUT': 60  # 请求超时
    }
    engine = get_engine()  # 连接数据库
    session = sessionmaker(bind=engine)
    sess = session()
    categorytasks = sess.query(CategoryTask.id, CategoryTask.category_link, CategoryTask.task_code, CategoryTask.plat,
                               CategoryTask.site, CategoryTask.link_maxpage) \
        .filter(and_(CategoryTask.plat == 'Mano', CategoryTask.status == None)).distinct()
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
        task_list = []
        count = 0
        for category in self.categorytasks:
            for page in range(1,category.link_maxpage+1):
            # for page in range(1, 4):
                task_list.append({"url": category.category_link + '?page=' + str(page),
                                  "meta": {'id': category.id, 'task_code': category.task_code,
                                            'plat': category.plat, 'site': category.site, 'page': page}})
                count += 1
                print('第'+str(count)+'条链接')
        for t in task_list:
            yield Request(url=t['url'], callback=self.parse, meta=t['meta'], headers=self.headers_html)

    def parse(self, response):
        # if response.status == 202:
        #     yield scrapy.Request(response.url, callback=self.parse, meta = response.meta, dont_filter=True)
        #     return

        id = response.meta['id']
        task_code = response.meta['task_code']
        plat = response.meta['plat']
        site = response.meta['site']
        page = response.meta['page']
        doc = pq(response.text)

        item_cate_list = []
        item_rank_list = []
        count = 0

        for d in doc('div[data-testid="products-layout-category"] a').items():
            item = {}
            count += 1
            href = d.attr('href')
            if 'fr' in site:
                href = 'https://www.manomano.fr' + href
            elif 'es' in site:
                href = 'https://www.manomano.es' + href
            elif 'it' in site:
                href = 'https://www.manomano.it' + href
            asin = extract_number(href[-8:])
            item['asin'] = asin
            item['create_time'] = datetime.now()
            item['plat'] = plat
            item['site'] = site
            item_cate = item.copy()
            # 换站点需要修改
            item_cate['href'] = href
            item_cate['cate_task_code'] = task_code
            item_cate['bsr_index'] = count
            item_cate_list.append(item_cate)

            item_rank = item.copy()
            item_rank['category1'] = ''
            item_rank['rank1'] = ''
            item_rank['category2'] = ''
            item_rank['rank2'] = ''
            item_rank['page_index'] = count
            item_rank['page'] = page
            price = d('span[data-testid="price-main"] span.c2nS1G8').text() + '.' + d('span[data-testid="price-main"] span.mnYZmE').text()
            item_rank['price'] = add_decimal(price)
            item_rank['reviews'] = extract_number(d('div.c4RbFAh.pWFNdu.VP-gp_.SZJsp3').text())
            item_rank['sp_tag'] = d('div.c5MHx7P.tIkne3 span.iq94bJ').text()
            rating = d('span.AFutZ6').attr('aria-label')
            if rating is not None:
                rating = rating[:3]
                if '/' in rating:
                    rating = rating[:1]
            item_rank['rating'] = rating
            item_rank_list.append(item_rank)

            item_attr = item.copy()
            brand = d('img[alt]').eq(1).attr('alt')
            item_attr['seller'] = brand
            item_attr['brand'] = brand
            item_attr['imghref'] = d('img.rhRMkC.Xoiu6o').attr('src')
            item_attr['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item_attr['update_time'] = item_attr['create_time']
            # print(item_attr)
            yield {'data': item_attr, 'type': 'asin_attr'}
        # print(item_rank_list)
        # sys.exit()
        yield {'data': {'id': id, 'page': page}, 'type': 'category_task'}
        yield {'data': item_cate_list, 'type': 'asin_task_add'}
        yield {'data': item_rank_list, 'type': 'asin_rank'}



