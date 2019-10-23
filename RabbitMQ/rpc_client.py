# rabbitmq RPC实现 客户端
import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        # 客户端启动时，创建回调队列，会开启会话用于发送RPC请求以及接受响应
        # 建立连接，指定服务器的ip地址
        credentials = pika.PlainCredentials('me', '123')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, '/', credentials))
        # 建立一个会话，每个channel代表一个会话任务
        self.channel = self.connection.channel()

        # 声明回调队列，再次声明的原因是，服务器和客户端可能先后开启，该声明是幂等的，多次声明，但只生效一次
        #exclusive=True 参数是指只对首次声明它的连接可见
        #exclusive=True 会在连接断开的时候，自动删除
        result = self.channel.queue_declare(queue='', exclusive=True)
        # 将队列指定为当前客户端的回调队列
        self.callback_queue = result.method.queue
        print(self.callback_queue)

        # 客户端订阅回调队列，当回调队列中有响应时，调用`on_response`方法对响应进行处理;
        # self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue) #PY2
        self.channel.basic_consume(self.callback_queue, self.on_response) #PY3

    # 对回调队列中的响应进行处理的函数
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    # 发出RPC请求
    # 例如这里服务端就是一个切菜师傅，菜切好了，需要传递给洗菜师傅，这个过程是发送rpc请求
    def call(self, n):
        # 初始化 response
        self.response = None
        # 生成correlation_id 关联标识，通过python的uuid库，生成全局唯一标识ID，保证时间空间唯一性
        self.corr_id = str(uuid.uuid4())
        # 发送RPC请求内容到RPC请求队列`rpcqueue`，同时发送的还有`reply_to`和`correlation_id`
        self.channel.basic_publish(exchange='',
                                   routing_key='rpcqueue',
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

# 建立客户端
fibonacci_rpc = FibonacciRpcClient()

# 发送RPC请求，丢进rpc队列，等待客户端处理完毕，给与响应
print(" [x] Requesting fib(30)")
# 发送一个RPC请求并阻塞直到获取结果
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % (response,))
