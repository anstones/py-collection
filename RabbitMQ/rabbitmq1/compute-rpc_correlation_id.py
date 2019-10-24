import pika
import sys

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, '/', credentials))
channel = connection.channel()

#定义队列
channel.queue_declare(queue='compute')
print(' [*] Waiting for n')

#将n值加1
def increase(n):
    # if n == 0:
    #     return 0
    # elif n == 1:
    #     return 1
    # else:
    #     return increase(n-1) + increase(n-2)
    return n+1

#定义接收到消息的处理方法
def request(ch, method, properties, body):
    print(" [.] increase(%s)"%(body,))
    response = increase(int(body))

    #将计算结果发送回控制中心
    ch.basic_publish(exchange='',
                        routing_key=properties.reply_to,
                        properties=pika.BasicProperties(
                            correlation_id=properties.correlation_id
                        ),
                        body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume('compute', request)

channel.start_consuming()