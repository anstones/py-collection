#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# apscheduler    python 定时任务库  可跨平台

from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.log',
                    filemode='a')


def aps_test(x):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)


now = datetime.datetime.now()
scheduler = BlockingScheduler()
scheduler._logger = logging
scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron', second='*/5')
scheduler.add_job(func=aps_test, args=('一次性任务',), next_run_time=now + datetime.timedelta(seconds=12))
scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', seconds=3)

scheduler.start()
