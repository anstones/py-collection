import pika
import sys

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, 'myhost', credentials))
channel = connection.channel()

#定义交换机，设置类型为topic
channel.exchange_declare(exchange='msg', exchange_type='topic')

#从命令行获取路由参数，如果没有，则报错退出
routings = sys.argv[1:]
if not routings:
    print >> sys.stderr, "Usage: %s [routing_key]..." % (sys.argv[0],)
    exit()

#生成临时队列，并绑定到交换机上，设置路由键
result = channel.queue_declare("", exclusive=True)
queue_name = result.method.queue
for routing in routings:
    channel.queue_bind(exchange='msg',
    queue=queue_name,
    routing_key=routing)

def callback(ch, method, properties, body):
    print("[x] Received %r" % (body,))

channel.basic_consume(queue_name, callback, auto_ack=True)

print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
