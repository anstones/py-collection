#连接redis
import time
import uuid
import redis
import traceback
from threading import Thread


redis_client = redis.Redis(host="192.168.133.128",
                           port=6379,
                           db=10)

#获取一个锁
# lock_name：锁定名称
# acquire_time: 客户端等待获取锁的时间
# time_out: 锁的超时时间
def acquire_lock(lock_name, acquire_time=10, time_out=10):
    """获取一个分布式锁"""
    identifier = str(uuid.uuid4())
    end = time.time() + acquire_time
    lock = "string:lock:" + lock_name
    while time.time() < end:
        if redis_client.setnx(lock, identifier):
            # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
            redis_client.expire(lock, time_out)
            return identifier
        elif not redis_client.ttl(lock):
            redis_client.expire(lock, time_out)
        time.sleep(0.001)
    return False

#释放一个锁
def release_lock(lock_name, identifier):
    """通用的锁释放函数"""
    lock = "string:lock:" + lock_name
    pip = redis_client.pipeline(True)
    while True:
        try:
            pip.watch(lock)
            lock_value = redis_client.get(lock)
            if not lock_value:
                return True

            if lock_value.decode() == identifier:
                pip.multi()
                pip.delete(lock)
                pip.execute()
                return True
            pip.unwatch()
            break
        except Exception as e:
            print("error:{}".format(traceback.format_exc()))
    return False


count=10

def seckill(i):
    identifier=acquire_lock('resource')
    print("线程:{}--获得了锁".format(i))
    time.sleep(1)
    global count
    if count<1:
        print("线程:{}--没抢到，票抢完了".format(i))
        return
    count-=1
    print("线程:{}--抢到一张票，还剩{}张票".format(i,count))
    release_lock('resource',identifier)


for i in range(50):
    t = Thread(target=seckill,args=(i,))
    t.start()