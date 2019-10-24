import pika
import sys

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, 'myhost', credentials))
channel = connection.channel()
 
channel.queue_declare(queue='task', durable=True)
 
message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='',
                      routing_key='task',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % (message,))
connection.close()