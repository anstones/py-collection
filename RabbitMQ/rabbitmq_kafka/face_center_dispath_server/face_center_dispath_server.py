import time
import traceback

from .rabbitmq_client import RabbitmqClient
from .dispath_center import DispatchCenter

RmqHost = "192.168.128.133"
RmqPort = 5672
RmqVHost = "oeasy_vhost_prod"
RmqUser = "oeasy"
RmqPassword = "oeasy"
ConsumeQueueName = "ConsumeQueueName"
dispatch_center_inst_ = DispatchCenter()

def start_rmq_listen():
    n_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s Rabbitmq Server start at the time: %s %s", "*" * 20, n_time, "*" * 20)

    rmq_client_ = RabbitmqClient(RmqHost, RmqPort, RmqVHost, RmqUser, RmqPassword)
    rmq_client_.start()

    while True:
        try:
            # 声明消息队列，消息将在这个队列中进行传递。如果将消息发送到不存在的队列，rabbitmq将会自动清除这些消息。如果队列不存在，则创建
            rmq_client_.channel.queue_declare(queue=ConsumeQueueName, durable=True)
            while True:
                # basic_get 消费消息，同basic_consume
                method, properties, body = rmq_client_.channel.basic_get(queue=ConsumeQueueName, no_ack=True)
                if all((method, properties, body)):
                    
                    dispatch_center_inst_.rmq_callback(rmq_client_.channel, method, properties, body)
                else:
                    time.sleep(5)
        except Exception as e:
            print(traceback.format_exc())
            print("rabbitmq error: %s", e)
            time.sleep(5)


def main():
    start_rmq_listen()
