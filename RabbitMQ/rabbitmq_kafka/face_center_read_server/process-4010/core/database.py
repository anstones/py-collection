#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from lib.lconf import Lconf
Global_lconf = Lconf()

mysql_address = 'mysql://{}:{}@{}:{}/{}'.format(Global_lconf.SevDbUser,
                Global_lconf.SevDbPassword,
                Global_lconf.SevDbHost,
                Global_lconf.SevDbPort,
                Global_lconf.SevDbDatabase)
                
engine = create_engine(mysql_address, convert_unicode=True, pool_recycle=20)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)

unit_cache = {}
def get_code_by_unit(unit_id):
    try:
        if int(unit_id) == 0: #全国黑名单  全部同步
            return (0,0,0)
        if unit_id in unit_cache:
            return unit_cache[unit_id]
        sql = "select province_code, city_code, town_code from t_pb_unit where id=%d" %int(unit_id)
        codes = db_session_biz.execute(sql)
        province_code =None
        for x in codes:
            province_code = x[0]
            city_code = x[1]
            town_code = x[2]
        if province_code is not None: 
            unit_cache[unit_id] = (province_code, city_code, town_code)
            return (province_code,city_code,town_code)
        else:
            return (None,None,None)
    except Exception as e:
        print("get failed,"+str(e))
        return (None, None, None)