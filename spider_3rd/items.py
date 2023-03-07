# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# orm 框架
from sqlalchemy import create_engine,Column,Integer,TIMESTAMP,Float,String,Table,MetaData
from sqlalchemy.ext.declarative import declarative_base

class Spider3RdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

from sqlalchemy.ext.declarative import declarative_base

# '__tablename__':'sp_plat_site_task'

Base = declarative_base()
Base.metadata.schema = 'spider'

class CategoryTask(Base):
    __tablename__ = 'sp_plat_site_task'
    id = Column(Integer, primary_key=True)#主键自增
    plat = Column(String(50))  # 平台
    site = Column(String(50))  # 站点
    salegroup = Column(String(50))  # 业务组
    saler = Column(String(50))  # 业务负责人
    category_cn = Column(String(50))  # 类目中文
    category_type = Column(String(10))  # 类目类型
    category = Column(String(100))  # 类目
    category1 = Column(String(100))  # 类目1
    category2 = Column(String(100))  # 类目2
    amzcategory = Column(String(50))  # 末级类目
    bsr_id = Column(String(50))  # 类目编号
    category_link_src = Column(String(200))  # 原始链接
    category_link = Column(String(200))  # 链接修正
    task_code = Column(String(50))  # 任务编码
    check_month = Column(String(10))  # 校验月份
    c_page = Column(Integer) #当前页
    status = Column(String(10))  # 状态 null crawled
    link_maxpage = Column(Integer) #最大页数
    update_time = Column(TIMESTAMP) #更新时间
    create_time = Column(TIMESTAMP) #创建时间
    category_cn_new = Column(String(50))  # 类目中文修复
    task_code_old = Column(String(50))  # 类目编码修复

# '__tablename__':'sp_plat_site_asin_info_task'

class AsinTask(Base):
    __tablename__ = 'sp_plat_site_asin_info_task'
    id = Column(Integer, primary_key=True)#主键自增
    plat = Column(String(50))  # 平台
    site = Column(String(50))  # 站点
    cate_task_code = Column(String(50))  # 任务编码
    href = Column(String(50))  # 链接
    sku = Column(String(50))  # SKU
    asin = Column(String(50))  # 平台编码
    sp_tag = Column(String(10))  # 平台编码
    bsr_index = Column(Integer) #页面排序
    status = Column(String(10)) #状态
    update_time = Column(TIMESTAMP) # 更新时间
    create_time = Column(TIMESTAMP) # 创建时间

# '__tablename__':'sp_plat_site_asin_attr'
class AsinAttr(Base):
    __tablename__ = 'sp_plat_site_asin_attr'
    id = Column(Integer, primary_key=True)#主键自增
    plat = Column(String(50))  # 平台
    site = Column(String(50))  # 站点
    sku = Column(String(50))  # sku
    asin = Column(String(50))  # 平台编码
    seller = Column(String(50))  # 卖家
    sellertype = Column(String(50))  # 卖家类型
    create_time = Column(TIMESTAMP) # 创建时间
    pasin = Column(String(50))  # 父编码
    brand = Column(String(100))  # 品牌
    shift_date = Column(TIMESTAMP) # 上架时间
    sp_tag = Column(String(100))  # 广告标识
    tag1 = Column(String(100))  # 标签1
    tag2 = Column(String(100))  # 标签2
    tag3 = Column(String(100))  # 标签3
    tag4 = Column(String(100))  # 标签4
    update_time = Column(TIMESTAMP) # 更新时间
    imghref = Column(String(255))  # 图片链接

# '__tablename__':'sp_plat_site_asin_rank_cd'

class AsinRankCD(Base):
    __tablename__ = 'sp_plat_site_asin_rank_cd'
    id = Column(Integer, primary_key=True)#主键自增
    plat = Column(String(50))  # 平台
    site = Column(String(50))  # 站点
    sku = Column(String(50))  # sku
    asin = Column(String(50))  # 平台编码
    rank1 = Column(Integer) # 排名1
    category1 = Column(String(50))  # 类目1
    rank2 = Column(Integer) # 排名2
    category2 = Column(String(50))  # 类目2
    price = Column(Float) # 价格
    create_time = Column(TIMESTAMP) # 创建时间
    estsales = Column(Float) # 推算销量
    selleroffers = Column(Integer) # 卖家数
    rating = Column(Float) # 评分
    reviews = Column(Integer) # 评价数
    sp_tag = Column(String(100))  # 广告标识
    page_index = Column(Integer) # 页面排序
    page = Column(Integer) #页数
    sellertype = Column(String(10))  # 卖家类型

class AsinRankMano(Base):
    __tablename__ = 'sp_plat_site_asin_rank_mano'
    id = Column(Integer, primary_key=True)#主键自增
    plat = Column(String(50))  # 平台
    site = Column(String(50))  # 站点
    sku = Column(String(50))  # sku
    asin = Column(String(50))  # 平台编码
    rank1 = Column(Integer) # 排名1
    category1 = Column(String(50))  # 类目1
    rank2 = Column(Integer) # 排名2
    category2 = Column(String(50))  # 类目2
    price = Column(Float) # 价格
    create_time = Column(TIMESTAMP) # 创建时间
    estsales = Column(Float) # 推算销量
    selleroffers = Column(Integer) # 卖家数
    rating = Column(Float) # 评分
    reviews = Column(Integer) # 评价数
    sp_tag = Column(String(100))  # 广告标识
    page_index = Column(Integer) # 页面排序
    page = Column(Integer) #页数
    sellertype = Column(String(10))  # 卖家类型

class AsinRankConforama(Base):
    __tablename__ = 'sp_plat_site_asin_rank_conforama'
    id = Column(Integer, primary_key=True)#主键自增
    plat = Column(String(50))  # 平台
    site = Column(String(50))  # 站点
    sku = Column(String(50))  # sku
    asin = Column(String(50))  # 平台编码
    rank1 = Column(Integer) # 排名1
    category1 = Column(String(50))  # 类目1
    rank2 = Column(Integer) # 排名2
    category2 = Column(String(50))  # 类目2
    price = Column(Float) # 价格
    create_time = Column(TIMESTAMP) # 创建时间
    estsales = Column(Float) # 推算销量
    selleroffers = Column(Integer) # 卖家数
    rating = Column(Float) # 评分
    reviews = Column(Integer) # 评价数
    sp_tag = Column(String(100))  # 广告标识
    page_index = Column(Integer) # 页面排序
    page = Column(Integer) #页数
    sellertype = Column(String(10))  # 卖家类型


