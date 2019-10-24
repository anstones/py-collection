import pika
import time

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, 'myhost', credentials))
channel = connection.channel()
 
channel.queue_declare(queue='task', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
 
def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    time.sleep(3)
    print (" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)
 
channel.basic_qos(prefetch_count=1)
channel.basic_consume('task', callback)
 
channel.start_consuming()