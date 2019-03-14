cd /home/oeasy/face_node_v5.2/face_compare_server/services

cp *service /etc/systemd/system
# 服务生效
systemctl enable face_compare.service face_detect.service face_lbs.service
# 立即启动服务
systemctl start face_compare.service face_detect.service face_lbs.service


# 5.2 版本及以上 100路部署：
/home/oeasy/face_node_v5.2/face_compare_server
compare: nohup /usr/bin/python algo_server.py compare > nohup/compare.log 2>&1 &
detect:  for i in `seq 0 11`; do let port=7000+$i; nohup /usr/bin/python algo_server.py detect $port $i > nohup/face_detect_$port.log 2>&1 & done
lbs: nohup /usr/bin/python algo_server.py lbs 7000 12 > nohup/lbs.log 2>&1 &
 #### nohup /usr/bin/python algo_server.py proxy 8008 0 &




# svn下载代码
1. svn co svn://zimg.0easy.com/face_node_v5_test/face_node_v5.2 
2. svn co svn://zimg.0easy.com/face_node_v5_facelib 对应模型移动至 oeasy_face_lib下
   wget https://qimg.0easy.com/1540965390915_144fd95ee91f7fc7f923f741774befbd.tar.gz?p=0 -O models.tar.gz
3. cd face_node_v5/conf/face_compare_server.conf 修改小区ID
4. pip uninstall tensorfolw tensorfolw_gpu
   pip install tensorflow==1.4.1 tensorflow_gpu==1.4.1 paho-mqtt numpy==1.14.5 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
5. cd /home/oeasy/face_node_v5.2/face_compare_server
  # 生成grpc服务文件
  python -m grpc_tools.protoc -I./protos --python_out=./rpc --grpc_python_out=./rpc compare.proto
   
6. 添加到守护进程：
   cd /home/oeasy/face_node_v5.2/face_compare_server/services
   cp *service /etc/systemd/system
   systemctl enable face_compare.service face_detect.service face_lbs.service
   systemctl start face_compare.service face_detect.service face_lbs.service


# svn用户名/密码
tom/123456


# 100路测试服务器
192.168.2.111
