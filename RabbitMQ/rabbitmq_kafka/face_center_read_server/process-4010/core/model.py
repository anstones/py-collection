#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Table, Column, Integer, String, PickleType, LargeBinary, ForeignKey, SmallInteger, DateTime
from sqlalchemy.orm import relationship, backref
from database import Base, db_session, get_code_by_unit
from lib.logger import logger

tags = Table('tags',
             Base.metadata,
             Column('user_id', Integer, ForeignKey('user.id')),
             Column('device_id', Integer, ForeignKey('device.id'))
             )


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uid = Column(String(254), unique=True, nullable=False)
    pic_md5 = Column(PickleType, unique=False, nullable=True)
    feature = relationship('Feature', backref='user', lazy='dynamic')
    devices = relationship('Device', secondary=tags, backref=backref('users', lazy='dynamic'), lazy='dynamic')

    province_code = Column(String(64), nullable=True)
    city_code = Column(String(64), nullable=True)
    town_code = Column(String(64), nullable=True)

    def get_city_info(self):
        devices_list = self.devices.all()
        if not devices_list:
            logger.warn("cant find city code with uid:%s", self.uid)
            return None, None, None
        return devices_list[0].province_code, devices_list[0].city_code, devices_list[0].town_code

    def __init__(self, uid, pic_md5=None, area=None, province_code=None, city_code=None, town_code=None):
        super(User, self).__init__()
        self.uid = uid
        self.pic_md5 = pic_md5
        if province_code is None and area is not None:
            province_code, city_code, town_code = get_code_by_unit(int(area))
        add_city_code(self, province_code, city_code, town_code)
        db_session.add(self)

    def __repr__(self):
        return '<User %r>' % self.uid


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey('area.id'))
    device = Column(String(254), unique=True, nullable=False)

    province_code = Column(String(64), nullable=True)
    city_code = Column(String(64), nullable=True)
    town_code = Column(String(64), nullable=True)

    def __init__(self, device):
        super(Device, self).__init__()
        area = device.split('_')[0]
        province_code, city_code, town_code = get_code_by_unit(area)
        self.device = device
        add_city_code(self, province_code, city_code, town_code)
        db_session.add(self)
        a = Area.query.filter_by(area=area).first()
        if not a:
            a = Area(area)
            add_city_code(a, province_code, city_code, town_code)
        a.devices.append(self)

    def __repr__(self):
        return '<Device %r>' % self.device


class Feature(Base):
    # __tablename__ = 'feature'
    __tablename__ = 'feature_model_0330'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(Integer, unique=False, nullable=False)
    feature_id = Column(Integer, unique=False, nullable=False)
    feature = Column(PickleType.impl(1024 * 1024), unique=False, nullable=False)

    province_code = Column(String(64), nullable=True)
    city_code = Column(String(64), nullable=True)
    town_code = Column(String(64), nullable=True)

    def __init__(self, timestamp, user, feature_id, feature):
        super(Feature, self).__init__()
        self.timestamp = timestamp
        self.user = user
        add_city_code(self, user.province_code, user.city_code, user.town_code)
        self.feature_id = feature_id
        self.feature = feature

    def __repr__(self):
        return '<Feature %d>' % self.feature_id


class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    area = Column(String(254), unique=True, nullable=False)
    auth_code = Column(String(254), unique=True, nullable=True)
    devices = relationship('Device', backref='area', lazy='dynamic')
    device_log = relationship('Device_log', backref='area', lazy='dynamic')
    user_log = relationship('User_log', backref='area', lazy='dynamic')

    province_code = Column(String(64), nullable=True)
    city_code = Column(String(64), nullable=True)
    town_code = Column(String(64), nullable=True)

    def __init__(self, area):
        super(Area, self).__init__()
        self.area = area

    def __repr__(self):
        return '<Area %r>' % self.area


class Device_log(Base):
    __tablename__ = 'device_log'
    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey('area.id'))
    timestamp = Column(Integer, unique=False, nullable=False)
    cmd = Column(String(254), unique=False, nullable=False)
    uid = Column(String(254), unique=False, nullable=False)
    device = Column(String(254), unique=False, nullable=False)
    start_time = Column(Integer, unique=False, nullable=False, default=0)
    end_time = Column(Integer, unique=False, nullable=False, default=0)

    province_code = Column(String(64), nullable=True)
    city_code = Column(String(64), nullable=True)
    town_code = Column(String(64), nullable=True)

    def __init__(self, timestamp, cmd, uid, device, start_time, end_time, province_code, city_code, town_code):
        super(Device_log, self).__init__()
        self.timestamp = timestamp
        self.cmd = cmd
        self.uid = uid
        self.device = device
        self.start_time = start_time
        self.end_time = end_time
        self.province_code = province_code
        self.city_code = city_code
        self.town_code = town_code

    def __repr__(self):
        return '<Device_log %r>' % self.area.area


class User_log(Base):
    __tablename__ = 'user_log'
    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey('area.id'))
    timestamp = Column(Integer, unique=False, nullable=False)
    uid = Column(String(254), unique=False, nullable=False)
    feature_id = Column(Integer, unique=False, nullable=False)

    province_code = Column(String(64), nullable=True)
    city_code = Column(String(64), nullable=True)
    town_code = Column(String(64), nullable=True)

    def __init__(self, timestamp, uid, feature_id, province_code, city_code, town_code):
        super(User_log, self).__init__()
        self.timestamp = timestamp
        self.uid = uid
        self.feature_id = feature_id
        self.province_code = province_code
        self.city_code = city_code
        self.town_code = town_code

    def __repr__(self):
        return '<User_log %r>' % self.area.area


class UserTags(Base):
    """
    用户标签， 分为三大类，
        1：白名单标签（业主， 家属，租户）
        2：黑名单标签（在逃人员，吸毒者）
        3：特殊关照人员（领导，传销...）
    """
    __tablename__ = 'user_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    area_code = Column(String(64), nullable=False)
    user_id = Column(Integer, nullable=False)
    type = Column(SmallInteger, nullable=False)
    tag = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, area_code, user_id, type, tag):
        self.area_code = area_code
        self.user_id = user_id
        self.type = type
        self.tag = tag

    def __repr__(self):
        return '<UserTags %s>' % self.user_id


def add_city_code(obj, province_code, city_code, town_code):
    obj.province_code = province_code
    obj.city_code = city_code
    obj.town_code = town_code
