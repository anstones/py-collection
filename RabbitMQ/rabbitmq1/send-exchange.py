import pika

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, 'myhost', credentials))
channel = connection.channel()

#定义交换机
channel.exchange_declare(exchange='messages', exchange_type='fanout')

#将消息发送到交换机
channel.basic_publish(exchange='messages', routing_key='', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()