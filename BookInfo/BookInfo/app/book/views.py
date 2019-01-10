#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.views import APIView, View
from rest_framework.response import Response
from django.http import HttpResponse
'''
# 第一种方法： 基于django和json序列化器，实现RESTFULL 接口风格
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
# Create your views here.
import json
from datetime import datetime
from .models import BookInfo

class BooksAPIVIew(View):
    """
    查询所有图书、增加图书
    """
    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
                'image': book.image.url if book.image else ''
            })
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
        新增图书
        路由：POST /books/ 
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            btitle=book_dict.get('btitle'),
            bpub_date=datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        )

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        }, status=201)

class BookAPIView(View):
    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.btitle = book_dict.get('btitle')
        book.bpub_date = datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        book.save()

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse(status=204)
'''
"""
# 第二种: 使用rest-framework.serializer.Serializer 类实现RESTFULL风格
from .serializers import BookInfoSerializer
...

"""

# 第三种： 使用rest-framework.serializer.ModelSerializer
"""
基于模型类自动生成一系列字段
基于模型类自动为Serializer生成validators，比如unique_together
包含默认的create()和update()的实现
"""
from .serializers import BookInfoASerializer
from .models import BookInfo
from rest_framework import status
from rest_framework.parsers import JSONParser


class BooksAPIVIew(APIView):

    def get(self, request, format=None):
        """
        通过APIView实现
        """
        try:    
            books = BookInfo.objects.all()
        except BookInfo.DoesNotExist:
            return status.HTTP_400_BAD_REQUEST
        serializer = BookInfoASerializer(books, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = JSONParser().parse(request)
        serializer = BookInfoASerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = JSONParser().parse(request)
        book = BookInfo.objects.get(id=data)
        serializer = BookInfoASerializer(book)
        serializer.delete()
        return status.HTTP_200_OK


