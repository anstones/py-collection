#!/usr/bin/env python
# coding:utf-8
import grpc
import time
from concurrent import futures
import lwz_model_pb2_grpc, lwz_model_pb2
 
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '6060'
 
class model(lwz_model_pb2_grpc.modelServicer):
    #### 随意定义-封装好的函数 #####
    def serch_student_class(self, index):
        if index == '201801':
            student_class = '5'
            return student_class
 
    def serch_student_grade(self,name ,age):
        if name =='lwz' and age == 100:
            student_grade = 100
            return student_grade
 
    ##### 真正重要的-输出函数 #####
    def lwz_show(self, request, context):
        index = request.index
        name = request.name
        age = request.age
 
        student_class = self.serch_student_class(index)
        student_grade = self.serch_student_grade(name ,age)
        print ("tansfer")
        return lwz_model_pb2.lwz_Response(stu_class = student_class,grade = student_grade)
 
def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lwz_model_pb2_grpc.add_modelServicer_to_server(model(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)
 
if __name__ == '__main__':
    serve()
