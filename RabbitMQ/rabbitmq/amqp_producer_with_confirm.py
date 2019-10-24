# coding=utf-8
import sys
import pika
# 支持消息确认

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, '/', credentials))
channel = connection.channel()

# 接收确认消息
channel.confirm_delivery()

channel.exchange_declare(exchange='web_develop', exchange_type='direct',
                         passive=False, durable=True, auto_delete=False)
if len(sys.argv) != 1:
    msg = sys.argv[1]
else:
    msg = 'hah'

props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
channel.basic_publish('web_develop', 'xxx_routing_key', msg, properties=props)
# connection.close()  # 关闭连接
