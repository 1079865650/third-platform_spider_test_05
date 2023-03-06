from sqlalchemy import create_engine,Column,Integer,TIMESTAMP,Float,String,Table,MetaData,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import db_env

def get_engine():
    # 默认为测试库
    engine = create_engine('postgresql+psycopg2://postgres:eya.psql.123456@eay-test-db-recovery-cluster.cluster-caa566iydlu9.rds.cn-northwest-1.amazonaws.com.cn:5432/bi', echo=False)  # 连接数据库
    # 设置生产切换为正式库
    if db_env == 'production':
        engine = create_engine('postgresql+psycopg2://spider:Xr6!g9I%40p5@52.83.104.99:5432/spider', echo=False)  # 连接数据库

    return engine
