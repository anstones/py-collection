from django.http import HttpResponse
from .models import Publish
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.http import StreamingHttpResponse
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger('django')

class PublishSerializers(serializers.Serializer):
    '''
    PublishSerializers 组件是一个集成功能组件
    到底用什么功能，取决于调用什么借口
    这是为PublishView做的组件，我们可以看出name，city，email都是Publish具有的
    '''
    name = serializers.CharField()
    city = serializers.CharField()
    email = serializers.CharField()


class PublishView(APIView):

    def get(self,request):
        publish_list = Publish.objects.all()
        ip = request.META["REMOTE_ADDR"]
        logger.debug("request ip %r", ip)
        # 方式一：Django序列化组件
        # ret=serialize("json",publish_list)

        # 方式二：REST序列化组件
        # 调用PublishSerializers组件把publish_list序列化
        # 这个组件不仅可以序列化QuerySet，也可以序列化一个model对象
        # 默认many=Flase 序列化model对象，many=True序列化QuerySet
        ps=PublishSerializers(publish_list, many=True)
        # 序列化完成的数据
        # ps.data
        return Response(ps.data)

    def post(self,request):
        pass


class DownloadFile(APIView):
    # 下载文件
    def get(self, request):
        file_name = request.GET["file_name"]
        the_file_name = BASE_DIR + os.sep + "/../" + 'static' + os.sep + file_name
        response = StreamingHttpResponse(self.file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name) 
        return response
    
    def file_iterator(self, file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    
    