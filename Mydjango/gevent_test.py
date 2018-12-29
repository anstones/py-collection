import socket
import gevent
from gevent import monkey;
monkey.patch_all()

urls = ['www.google.com', 'www.example.com', 'www.python.org']
# 使用的列表解析的方式形成list，而是不需要使用for和append的冗余代码区生成，简洁
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=2)
print([job.value for job in jobs])