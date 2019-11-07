#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import zlib
from lib.logger import logger
from models import Area, Device_log, User_log, User


class Feature(object):
    def get_feature(self, area, devices_request, timestamp, mac_address, add_del_done=0, limit=50, ttl=0):
        timestamp = int(timestamp if timestamp else time.time())
        last_record_time = -1  # 查询到的最后一条记录的时间

        result = []
        update_feature_done = 0

        user_msg_num = 0
        logger.info("get data start, area: %s, devices_request: %s", str(area), str(devices_request))

        area_record = Area.query.filter_by(area=area).first()
        if not area_record:
            logger.info("not area %s info", area)
            return json.dumps(result)

        data = []
        uls = area_record.user_log.filter(User_log.timestamp >= timestamp).order_by(User_log.timestamp).limit(
            limit).all()
        for ul in uls:
            last_record_time = ul.timestamp
            u = User.query.filter_by(uid=ul.uid).first()
            if u:
                # 根据传入的device过滤,不传时取全部数据
                if devices_request:
                    u_devices = [d.device for d in u.devices]
                    if set(u_devices) & set(devices_request) == set():
                        logger.warn("user %s filtered by request device %s", u, devices_request)
                        continue
                for f in u.feature.all():
                    data.append(
                        {'uid': ul.uid, 'pic_md5': u.pic_md5, 'feature_id': f.feature_id, 'feature': f.feature})

        if not uls or len(uls) < limit:
            update_feature_done = 1

        if data:
            user_msg_num += len(data)
            result.append({'type': 'update_feature', 'timestamp': last_record_time, 'data': data,
                           'update_feature_done': update_feature_done})
        else:
            result.append({'timestamp': last_record_time, 'data': [], 'update_feature_done': update_feature_done})

        logger.info("get feature data end, area:%s, user_msg_num:%d" % (area, user_msg_num))

        device_msg_num = 0
        if not add_del_done:
            result.append({'timestamp': last_record_time, 'add_del_done': 1})
            for cmd in ['add_user', 'del_user']:
                data = {}
                for dl in area_record.device_log.filter(
                        (Device_log.timestamp > timestamp) & Device_log.cmd.__eq__(cmd)):
                    if devices_request and dl.device not in devices_request:
                        # print("device_log %s filtered by request device %s" %
                        #       (dl, devices_request))
                        continue
                    uid = dl.uid

                    if ttl:  # 需要同步有效期
                        relation = {
                            "uid": uid,
                            "start_time": dl.start_time,
                            "end_time": dl.end_time
                        }
                        data.setdefault(dl.device, []).append(relation)

                    else:  # 不需要同步有效期
                        data.setdefault(dl.device, []).append(uid)
                if data:
                    device_msg_num += 1
                    result.append({'type': cmd, 'timestamp': last_record_time, 'data': data, 'add_del_done': 1})

        logger.info("get user data end, area:%s, device_msg_num:%d", area, device_msg_num)

        # return zlib.compress(json.dumps(result))
        return json.dumps(result)



