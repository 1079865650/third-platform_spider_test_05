# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, Float, String, Table, MetaData, and_
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .items import *
from .db_utils import *
from dateutil.relativedelta import relativedelta


class Spider3RdPipeline:
    def process_item(self, item, spider):
        return item


class TaskSpidersPipeline(object):
    def __init__(self):  # 执行爬虫时
        self.engine = get_engine()  # 连接数据库
        self.session = sessionmaker(bind=self.engine)
        self.sess = self.session()

        # 动态创建orm类,必须继承Base, 这个表名是固定的,如果需要为每个爬虫创建一个表,请使用process_item中的
        self.CategoryTask = CategoryTask
        self.AsinTask = AsinTask

    def process_item(self, item, spider):  # 爬取过程中执行的函数

        if item['type'] == 'category_task':
            # print(item['data']['task_code'])
            self.sess.query(self.CategoryTask).filter(self.CategoryTask.id == item['data']['id']).update({"status": 'crawled', 'c_page': item['data']['page'], 'update_time': datetime.now()})
            self.sess.commit()
            return item
        elif item['type'] == 'asin_task_add':
            for i in item['data']:
                self.sess.add(self.AsinTask(**i))
            self.sess.commit()
            return item
        else:
            return item

    def close_spider(self, spider):  # 关闭爬虫时
        self.sess.close()


class AsinSpidersPipeline(object):
    def __init__(self):  # 执行爬虫时
        self.engine = get_engine()  # 连接数据库
        self.session = sessionmaker(bind=self.engine)
        self.sess = self.session()

        # 动态创建orm类,必须继承Base, 这个表名是固定的,如果需要为每个爬虫创建一个表,请使用process_item中的
        self.AsinTask = AsinTask
        self.AsinAttr = AsinAttr
        self.AsinRankCD = AsinRankCD
        self.AsinRankMano = AsinRankMano
        self.AsinRankConforama = AsinRankConforama

    def process_item(self, item, spider):  # 爬取过程中执行的函数

        # 更新抓取asin状态
        if item['type'] == 'asin_task':
            self.sess.query(self.AsinTask).filter(and_(self.AsinTask.id == item['data']['id'])).update({"status": 'crawled','update_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            self.sess.commit()
            return item

        # 删除老属性 新增新属性
        elif item['type'] == 'asin_attr':
            # 删除新增
            self.sess.query(self.AsinAttr).filter(and_(self.AsinAttr.site == item['data']['site'], self.AsinAttr.asin == item['data']['asin'])).delete()
            self.sess.add(self.AsinAttr(**item['data']))
            self.sess.commit()
            return item
        
        # 插入新的时序数据
        elif item['type'] == 'asin_rank':
            for i in item['data']:
                if i['plat'] == 'CD':
                    self.sess.add(self.AsinRankCD(**i))
                    self.sess.commit()
                if i['plat'] == 'Conforama':
                    # 判断asin_rank 是列表页抓取还是详情页抓取  详情页有price,rating 列表页没有
                    if 'price' in i and 'rating' in i:
                        # 给price一个默认值
                        if i["price"] == None:
                            i["price"] = '0'
                            # 从asin_rank中修改表数据  列表页已经写入了一部分数据
                        self.sess.query(self.AsinRankConforama).filter(and_(self.AsinRankConforama.plat == i['plat'],
                                                                            self.AsinRankConforama.asin == i['asin'],
                                                                            self.AsinRankConforama.price == None,
                                                                            self.AsinRankConforama.create_time > (datetime.now() + relativedelta(days=0)).strftime("%Y-%m-%d")
                                                                            )) \
                            .update({"price": i['price'], "rating": i['rating'], "reviews": i['reviews'], "create_time": i["create_time"]})
                        # self.sess.add(self.AsinRankConforame(**i))
                        self.sess.commit()
                    else:
                        self.sess.add(self.AsinRankConforama(**i))
                        self.sess.commit()
                if i['plat'] == 'Mano':
                    self.sess.add(self.AsinRankMano(**i))
                    self.sess.commit()
            return item

        elif item['type'] == 'asin_rank_single':
            self.sess.add(self.AsinRankConforama(**item['data']))
            self.sess.commit()

        elif item['type'] == 'asin_img':
            for i in item['data']:
                if i['plat'] == 'CD':
                    v_list = self.sess.query(self.AsinAttr).filter(and_(self.AsinAttr.site == i['site'], self.AsinAttr.asin == i['asin'])).all()
                    try:
                        for v in v_list:
                            v.imghref = i['imghref']
                    except:
                        print(i)

                    self.sess.commit()
            return item
        else:
            return item

    def close_spider(self, spider):  # 关闭爬虫时
        self.sess.close()
