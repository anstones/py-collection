import pika

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, 'myhost', credentials))
channel = connection.channel()

#定义交换机
channel.exchange_declare(exchange='messages', exchange_type='fanout')

#随机生成队列，并绑定到交换机上
result = channel.queue_declare("", exclusive=True)

queue_name = result.method.queue
channel.queue_bind(exchange='messages', queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))

channel.basic_consume(queue_name, callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
