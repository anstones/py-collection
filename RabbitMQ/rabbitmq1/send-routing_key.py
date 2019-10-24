import pika

credentials = pika.PlainCredentials('oeasy', 'oeasy')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, 'myhost', credentials))
channel = connection.channel()

#定义交换机，设置类型为direct
channel.exchange_declare(exchange='message', exchange_type='direct')
 
#定义三个路由键
routings = ['info', 'warning', 'error']
 
#将消息依次发送到交换机，并设置路由键
for routing in routings:
    message = '%s message.' % routing
    channel.basic_publish(exchange='message',
                          routing_key=routing,
                          body=message)
    print(message)
 
connection.close()