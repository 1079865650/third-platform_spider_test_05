import sys

import scrapy
from ..parse_utils import *
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, Float, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
from scrapy import Request
from ..items import *
from ..db_utils import *
from sqlalchemy.orm import sessionmaker
from pyquery import PyQuery as pq
from datetime import datetime


class SpiderConforamaSpider(scrapy.Spider):
    name = 'spider_conforama_category'

    custom_settings = {
        'LOG_LEVEL': 'INFO',  # 日志级别
        'DOWNLOAD_DELAY': 5,  # 抓取延迟
        'CONCURRENT_REQUESTS': 20,  # 并发限制
        'DOWNLOAD_TIMEOUT': 60  # 请求超时
    }
    engine = get_engine()  # 连接数据库
    session = sessionmaker(bind=engine)
    sess = session()
    categorytasks = sess.query(CategoryTask.id, CategoryTask.category_link, CategoryTask.task_code
                               , CategoryTask.plat, CategoryTask.site, CategoryTask.link_maxpage) \
        .filter(CategoryTask.plat == 'Conforama', CategoryTask.status == None).distinct()
    sess.close()
    headers_html = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-Encoding': "gzip, deflate, br",
        'accept-Language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache",
        'pragma': "no-cache",
        # 'cookies': 'i18n-prefs=EUR; session-id=262-9901611-0924745; ubid-acbde=259-3941084-5286836; session-token=qhDFSEZ6+ccIuF2ilS1/iAYerK0K/ASj6BanWofymzMzAc5Vm53bqv1NQgwA1LGaOxtKzOEhJkVY0grbwqlOUAyoctgO5YA1KIe1RMuwA7R3WrRT5YJbuI0Roln6QLCX2qii7uOw49riDdBWLn6H2hlNX2PRA9sxx6Y0qPN44xWa86NdvrZMRtpO5CntkagC; csm-hit=adb:adblk_no&t:1641966024138&tb:s-2KNW0G61T7QBH5XE9EYW|1641966021900; session-id-time=2082754801l',
        # 'cookies': 'session-id-time=2082787201l; session-id=139-1554758-4776217; ubid-main=131-5304300-2410331; i18n-prefs=USD; session-token=zy5al9bokAW735EECAk/urNgIW82HwgQkN8ViOU0J0wpwPx2P7/OXvNVGYo5K2tc5HjcUIay722+N+PE4HaN1dOlN18cl6QXAFpdO/rmKpO3BqTaIbB36uwhvS9UDb0sQQeg8B5FJpMRWtaeZ/jEyAilSBTKrd8qiZcVRkkSW9Jr+5U3XcpPMiNLMYl+VNmr; csm-hit=tb:T6P7P77AH687TE54B8HE+s-YE5MFBJKTKWBQP29D8GN|1639728118958&t:1639728118958&adb:adblk_no',
        'sec-ch-ua': "\";Not A Brand\";v=\"99\", \"Chromium\";v=\"88\"",
        # 'cookie': 'cs_heure_session=12; _schn=_5677tz; CookieId=CookieId=221226090520COSPFLMJ&IsA=0; TC_AB=B; SitePersoCookie=PersoCountryKey____PersoLatitudeKey____PersoLongitudeKey____PersoTownKey____GeolocPriorityKey__0__PersoPostalCodeKey____PersoUrlGeoSCKey____ExpressSellerId____ExpressShopName____ExpressGlobalSellerId____ShowroomVendorId____RetailStoreName____VehicleId__0__AddressId____; s_ecid=MCMID%7C78681200637328983069213085287547091337; tcId=49954fe9-a7b4-457d-a96b-64041d22bca6; UniqueVisitContext=UniqueVisitId__221226090539DBWQXPGG__; TCPID=122121165395848157544; app_vi=34214400%7C; prio30j=prio3; _cs_c=3; TC_PRIVACY=0@078%7C2%7C2%7C176@4%2C1%2C5%2C3%2C2%2C6%2C10001%2C10003%2C10005%2C10007%2C10013%2C10015%2C10017%2C10019%2C10009%2C10011%2C13002%2C13001%2C10004%2C10014%2C10016%2C10018%2C10020%2C10010%2C10012%2C10006%2C10008@@1672041988836%2C1672041988836%2C1687593988836@_u_PvZ8a-F4BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACKqOn6gO_u-YujiLKfB6576K-C69kmqC-amoFqaKCY8KqbrzqmGjqi4oYACg7gBoh6oHkMrqIGgKhgIPirmOPvYe4BiK7XmwcYKg6KgLioaiaCYuIDYGIoGOgHgmAungimABgCCACKghiooEGoiQGgiGEoGpAnYCAIiCgiGBKo4oAigqApoCCGCBqaYAKCKg6AgSAYghsKKBgvCoeKOAAogOiKom8oWgiIALorCABiKLCGoqiHq4uKi4uzTvgoEKo6sqiuqziquubhurngiq6xqvGZjHqojxqKKrn5uqGqirEo4EpgAQ%3D%3D; TC_PRIVACY_CENTER=4%2C1%2C5%2C3%2C2%2C6%2C10001%2C10003%2C10005%2C10007%2C10013%2C10015%2C10017%2C10019%2C10009%2C10011%2C13002%2C13001%2C10004%2C10014%2C10016%2C10018%2C10020%2C10010%2C10012%2C10006%2C10008; _$1okcook=1; _$cst=1; tcIdNe=f15a2dbe-4e95-456a-93bd-39858b9e1feb; _gcl_au=1.1.1138816586.1672041990; _scid=86ee1017-9be6-46ab-a7e1-34aaf8930e41; mics_vid=31407153870; SiteVersionCookieNoChanges=1370.1|1418.1|1423.1|1426.1|1433.1|1441.1|1458.1|1464.0|1466.1|1467.1|1469.1|1475.1|1482.1|1484.1|1488.1|1491.1|5008.1|5010.1|5011.1|5012.0|5013.1|5015.1|5016.0|5019.1|5021.1|5023.1|5024.1|5030.0|5033.1; __gsas=ID=10b6680c3c5efa4a:T=1672045865:S=ALNI_MYV8qFrf-0FC6Vzm0O04NmIqzwnhw; __gads=ID=202c717f0f960cc4:T=1672045869:S=ALNI_MY2v_0nXw_xssaDPsNXGy5zS2nQ4g; _fbp=fb.1.1672045872143.2091934392; _$dtype=t:d; mssctse=W2dNXeEyrPImiBMI1p4Mst16N_Fv-Uy8IcvQOQu8bmBQo6IT8RUh2z2t_oXR8RK1cbVKgCviFugxE3WhpY-P8Q; SiteVersionCookie=1547.1|2038.1|2524.1|3027.0|3032.1|3033.1|3040.0|4012.1|4018.1|4019.1|4026.1|4028.1|4033.0|4039.1|4302.1|4305.1|4308.1|4513.1|4514.1|4517.1|4521.0|4525.1; dtCookie=v_4_srv_21_sn_49B1F422595CE46BCD9AED13789DB6E2_perc_100000_ol_0_mul_1_app-3Ac93cbedcccfc6fbb_0; AMCV_6A63EE6A54FA13E60A4C98A7%40AdobeOrg=1585540135%7CMCIDTS%7C19367%7CMCMID%7C78681200637328983069213085287547091337%7CMCAID%7CNONE%7CMCOPTOUT-1672049130s%7CNONE%7CvVersion%7C4.4.0; svisit=1; _$3custinf=AUT=0&XV1=0; _$3ci=; prio7j=prio4; chcook7=direct; s_cc=true; _sctr=1|1673193600000; __gpi=UID=00000b97b92e50a7:T=1672045869:RT=1673239127:S=ALNI_MbZrIsRAE0xH78OzxSvPhgFCqvq6w; msswt=; el2=0; _cs_cvars=%7B%228%22%3A%5B%22h_deb_session%22%2C%2212%22%5D%7D; _MFB_=fHwxfHx8W118fHw1MC42MDM2NjgyMzYyNjk4MDR8; cache_cdn=; msstvt=Vw-lIBtQ-OFZ1RZ0GAg9fXLXyXNiD1tHYiQeJudtiXGoiE57AILLry3CpDGVBfMZ4-7NBQGVsmg3qZdlkzX-y81mn8--4dF2Q-ZQG67p4rXzofa3DxOqzxLAvZpgzNuQ2xoTjNOaY9EqSmnUosXU1w; cto_bundle=5hmx5V9FemxheTR4UyUyRmlWJTJGOTJ1JTJGVmZoS2tIQ3puNDEwU2dQNWZqSiUyQkQxUWtURmh4N09rVkhKaGJkQUxVJTJCcCUyRkFhNk5rY29rWVN4S1lhTjZpMXVZdTA5ZHpENjVQNnJteFJqTVJhSlViQU0lMkJOYWRDUGJBSnBpcEdybnJVcnJaZlZTZm9vUWVYaENsajR6bG9qcFBwZkZ4MWdPdyUzRCUzRA; mics_lts=1672041996238; cs_heure_session=12; s_pv=Page%20Erreur%20ErrorPage_webshop_404; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.cdiscount.com%252Fsearch%252F10%252Fbiblioth%25C3%25A8que.html%2523_his_; ABTasty=uid=bx0k59kakxk5zcw1&fst=1672041991188&pst=1672045866102&cst=1673239122970&ns=3&pvt=11&pvis=4&th=710841.882596.1.1.1.1.1672046106447.1672046106447.1.NaN_887959.1106086.9.2.3.1.1672041993011.1673239185158.1.3_888659.1106982.4.4.1.1.1672046067979.1673239185144.1.3_908953.1133635.11.4.3.1.1672041992005.1673239215467.1.3; _uetsid=7ed093b08fd711ed8c4a2dda80f99e45; _uetvid=34875a2084f411eda95e0b028ccfb188; s_nr=1673239215709-Repeat; _cs_id=862123cb-0f53-afc1-c901-b13723b9869d.1672041940.4.1673239218.1673239155.1590586488.1706205940404; _cs_s=2.5.0.1673241018316; tp=16230; s_ppv=Recherche%2C93%2C79%2C15048; VisitContextCookie=g3T0QkKkfmLLPzF9KvqRK4BN4_eWJW3Vd0wYVhpnp44oveXkmR9r5A; visit_baleen_ACM-655d43=JmNaL4p84LHEfek6eFD6LXyGs_pbLJ0bzcs2rXK8ua8rafvFRHH04TM1E5QmuDjZWdQDtliVRrEBT59k_SjsXFY3jn-a8wPKRF8oFimVR8jgw7SJlAnhOsVoxaEDM83-KnkM8WeMYlbBEBU5kYcjoDUTb6U1_YdOdUmLCxev02pEACl_JsWKSXvLGfQywFoezhtwDMPbYBKR9gN7glD1HHeW7qLWF7T3AFhpBAGw72JmqG_Zu8QFlyLUN1rVmUs9',
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
        print(self.categorytasks)
        count = 0
        for category in self.categorytasks[:5]:
            for page in range(1, category.link_maxpage+1):
            # for page in range(1, 5):
                task_list.append({"url": category.category_link + '&page=' + str(page),
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

        for d in doc('div.awk-descent-products.grid li[data-id]').items():
            item = {}
            count += 1
            item['asin'] = d.attr('data-id')
            item['create_time'] = datetime.now()
            item['plat'] = plat
            item['site'] = site

            item_cate = item.copy()
            item_cate['href'] = d('a.bindEvent.extendLink').attr('href').split('?')[0]
            item_cate['cate_task_code'] = task_code
            item_cate['bsr_index'] = count

            # print(item_cate)
            if 'sponsor' in d('.c-mention').text().lower():
                item_cate['sp_tag'] = 'sp'
            item_cate_list.append(item_cate)


            item_rank = item.copy()
            item_rank['category1'] = ''
            item_rank['rank1'] = ''
            item_rank['category2'] = ''
            item_rank['rank2'] = ''
            # price = extract_price(d('div.el-bottom.bottomBlocComponent div.price-product.typo-prix.eco-price').text())
            # item_rank['price'] = price
            # item_rank['rating'] = ''
            # item_rank['reviews'] = ''
            # item_rank['sp_tag'] = ''
            # item_rank['sellertype'] = ''
            # sp_tag = d('div.detail-product div.c-r_seller div.c-r_sold.c-r_sold--other span')
            # if sp_tag != '' and sp_tag is not None:
            #     item_rank['sp_tag'] = 'sp'
            item_rank['sellertype'] = d('div.detail-product div.c-r_seller div.c-r_sold.c-r_sold--other span').text()
            item_rank['page_index'] = count
            item_rank['page'] = page
            # if 'sponsor' in d('.c-mention').text().lower():
            #     item_rank['sp_tag'] = 'sp'
            # if 'discount à volonté' in d('.productCenterZone').text():
            #     item_rank['sellertype'] = 'FBC'
            item_rank_list.append(item_rank)
        # print(item_rank_list)
        # sys.exit()

        yield {'data': {'id': id, 'page': page}, 'type': 'category_task'}
        yield {'data': item_cate_list, 'type': 'asin_task_add'}
        yield {'data': item_rank_list, 'type': 'asin_rank'}
