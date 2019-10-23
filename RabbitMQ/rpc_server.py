# rabbitmq RPC实现 服务端
import pika

credentials = pika.PlainCredentials('me', '123')
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, '/', credentials))
except Exception as e:
    print(e)
else:
    channel = connection.channel()
    channel.queue_declare(queue='rpcqueue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    n = int(body)
    print("routing_key:{}, correlation_id:{}".format(props.reply_to, props.correlation_id))
    print("fib(%s)"  % (n,))
    # 调用数据处理方法
    response = fib(n)
    # 将处理结果(响应)发送到回调队列
    ch.basic_publish(exchange='',
                     # reply_to代表回复目标
                     routing_key=props.reply_to,
                     # correlation_id（关联标识）：用来将RPC的响应和请求关联起来。
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

# 负载均衡，同一时刻发送给该服务器的请求不超过一个
channel.basic_qos(prefetch_count=1)
channel.basic_consume('rpcqueue', on_request)

print(" [x] Awaiting RPC requests")
#开始消费
channel.start_consuming()
