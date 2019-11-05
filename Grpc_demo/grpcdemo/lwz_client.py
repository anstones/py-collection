import grpc
import lwz_model_pb2_grpc, lwz_model_pb2
 
_HOST = 'localhost'
_PORT = '6060'
 
def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = lwz_model_pb2_grpc.modelStub(channel=conn)
    response = client.lwz_show(lwz_model_pb2.lwz_Request(index = '201801',name = 'lwz',age = 100))
    print("received: " + response.stu_class)
    print("received: " + str(response.grade))
 
if __name__ == '__main__':
    run()
