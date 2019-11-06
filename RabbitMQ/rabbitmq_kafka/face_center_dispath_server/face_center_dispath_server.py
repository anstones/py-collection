import time
import traceback


from lib.lconf import Lconf
from lib.logger import logger
from lib.rabbitmq_client import RabbitmqClient
from core.dispath_center import DispatchCenter

Global_lconf = Lconf()

dispatch_center_inst_ = DispatchCenter()

def start_rmq_listen():
    n_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logger.info("%s Rabbitmq Server start at the time: %s %s", "*" * 20, n_time, "*" * 20)

    rmq_client_ = RabbitmqClient(Global_lconf.RmqHost, 
                                    Global_lconf.RmqPort, 
                                    Global_lconf.RmqVHost, 
                                    Global_lconf.RmqUser, 
                                    Global_lconf.RmqPassword
                                    )
    rmq_client_.start()

    while True:
        try:
            # 声明消息队列，消息将在这个队列中进行传递。如果将消息发送到不存在的队列，rabbitmq将会自动清除这些消息。如果队列不存在，则创建
            rmq_client_.channel.queue_declare(queue=Global_lconf.ConsumeQueueName, durable=True)
            while True:
                # basic_get 消费消息，同basic_consume
                method, properties, body = rmq_client_.channel.basic_get(queue=Global_lconf.ConsumeQueueName, no_ack=True)
                if all((method, properties, body)):
                    
                    dispatch_center_inst_.rmq_callback(rmq_client_.channel, method, properties, body)
                else:
                    time.sleep(5)
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("rabbitmq error: %s", e)
            time.sleep(5)


def main():
    start_rmq_listen()
