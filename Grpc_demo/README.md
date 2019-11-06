### GRPC demo
-  编译 protobuf
```
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. .abc.proto // abc.proto定义入参和出参
    python -m grpc_tools.protoc -I. --python_out=. –-grpc_python_out=. ./data.proto
```

- 参数说明
```
    python -m grpc_tools.protoc -I. --python_out=./rpc --grpc_python_out=./rpc ./kafka_push.proto
    # 命令解析(. 为执行命令所在的文件夹位置)
    python -m grpc_tools.protoc -I

    #指定proto所在的文件夹
    .

    # 请求和响应的数据格式类的位置helloworld_pb2.py
    --python_out=./rpc

    # 服务端、客户端类的位置helloworld_pb2_grpc.py
    --grpc_python_out=./rpc

    # 指定具体proto文件的位置
    ./kafka_psuh.proto
```