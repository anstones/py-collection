import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('me', '123')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128',5672,'myhost',credentials))
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.133.128'))
        self.channel = self.connection.channel()

        # self.channel.confirm_delivery() # 设置发送方确认机制，实现消息确认
        # self.num = 0
        # for i in range(10):
        #     ack = self.channel.basic_publish(body=str(self.num),
        #                                      exchange="",
        #                                      routing_key="rpc_queue")
        #     if ack == True:
        #         print "put message to rabbitmq successed!"
        #     else:
        #         print "put message to rabbitmq failed"

        # self.channel.tx_select() #设置信道为事务机制，实现消息确认
        # self.num = 0
        # for i in range(10):
        #     try:
        #         self.channel.basic_publish(exchange='',
        #                                     routing_key="rpc_queue",
        #                                     body = str(self.num))
        #         self.channel.tx_commit() # 提交事务操作
        #     except Exception as e:
        #         print("basic_publish error: {}".format(err))
        #         self.channel.tx_rollback() # 捕捉错误，回滚事务

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        print(self.callback_queue)

        # self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue) #PY2
        self.channel.basic_consume(self.callback_queue, self.on_response) #PY3

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % (response,))
