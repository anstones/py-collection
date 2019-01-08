# coding:utf-8
# how to use sqlalchemy


from sqlalchemy import create_engine

HOSTNAME = '192.168.6.192'
PORT = '3306'
DATABASE = 'mine'
USERNAME = 'root'
PASSWORD = 'mysql'

db_url = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    DATABASE
)

engine = create_engine(db_url)
# 创建映像
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(engine)
# 创建会话
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)
session = Session()

# if __name__ == '__main__':
#     print(db_url)