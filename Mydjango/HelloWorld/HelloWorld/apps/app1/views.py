from django.http import HttpResponse
from .models import Publish
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
import logging

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