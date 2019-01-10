#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import BookInfo
from rest_framework.views import APIView


class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)

    # 校验方法： 对特定字段：btitle进行校验
    def validate_btitle(self, value):
        if 'django' not in value.lower():
            raise serializers.ValidationError("图书不是关于Django的")
        return value

    # 校验方法：对多个字段校验
    def validate(self, attrs):
        bread = attrs['bread']
        bcomment = attrs['bcomment']
        if bread < bcomment:
            raise serializers.ValidationError('阅读量小于评论量')
        return attrs

    # 基于validated_data 新建对象（也可将对象一并保存到数据库）
    def create(self, validated_data):
        """新建"""
        # return BookInfo(**validated_data)
        return BookInfo.objects.create(**validated_data) # 存入数据库

    # 基于validated_data 更新对象（也可将对象一并保存到数据库）
    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.save() # 存入数据库
        return instance



class BookInfoASerializer(serializers.ModelSerializer):
    """图书数据序列化器"""

    # hbook = BookInfoSerializer(many=True)                # 指明显示的字段
    class Meta:
        model = BookInfo
        fields = '__all__'                               # 全部字段
        # fields = ('id', 'btitle', 'bpub_date')         # 指明为模型类的哪些字段生成
        # read_only_fields = ('id', 'bread', 'bcomment') # 指明那些字段为只读，配合fileds
        # exclude = ('image',)                           # 指明排除那些字段

        # extra_kwargs = {
        #     'bread': {'min_value': 0, 'required': True},
        #     'bcomment': {'max_value': 0, 'required': True}
        # }                                              # 使用extra_kwargs参数为ModelSerializer添加或修改原有的选项参数
