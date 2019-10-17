"""
简单的socket编程
"""
from socket import socket

# 服务端
server = socket()
server.bind(('127.0.0.1', 8000))
server.listen(5)
while True:
    conn, addr = server.accept()
    while True:
        data = conn.recv(1024)
        print(data.decode('utf-8'))
        conn.send(data.upper())
    conn.close()
server.close()


# 客户端
client = socket()
client.connect(('127.0.0.1', 8000))
while True:
    msg = input('>>>:').strip()
    if not msg:
        continue
    client.send(msg.encode('utf-8'))
    data = client.recv(1024).decode('utf-8')
    print('服务器已经收到信息并转换为大写', data)
client.close()
