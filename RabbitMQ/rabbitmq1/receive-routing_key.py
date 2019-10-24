import pika
import sys

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, 'myhost', credentials))
channel = connection.channel()

#定义交换机
channel.exchange_declare(exchange='message', exchange_type='direct')

#从命令行获取路由键参数，如果没有，则设置为info
routings = sys.argv[1:]
if not routings:
    routings = ['info']
 
#生成临时队列，并绑定到交换机上，设置路由键
result = channel.queue_declare("", exclusive=True)
queue_name = result.method.queue
for routing in routings:
    channel.queue_bind(exchange='message',
                       queue=queue_name,
                       routing_key=routing)
 
def callback(ch, method, properties, body):
    print("[x] Received %r" % (body,))
 
channel.basic_consume(queue_name, callback, auto_ack=True)
 
print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


