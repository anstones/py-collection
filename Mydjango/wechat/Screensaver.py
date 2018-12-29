# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 获取点赞好友头像,生成屏保
import os, random, math
import itchat
from PIL import Image


# 实现获取朋友指定信息的方法
def get_key_info(friends_info, key):
    return list(map(lambda friend_info: friend_info.get(key), friends_info))


# 获取朋友的相关信息，生成一个 {key:[value1,value2,...],} 类型的字典，最后返回该字典
def get_friends_info(friends):
    friends_info = dict(
        username=get_key_info(friends, 'UserName'),  # 用户名
    )
    return friends_info


# 保存微信好友的头像到本地
def get_head_img(friends):
    friends_info = get_friends_info(friends)
    username = friends_info['username']

    for i, uname in enumerate(username):
        with open("headImgs/" + str(i) + ".png", "wb") as f:
            img = itchat.get_head_img(uname)  # itchat.get_head_img() 获取到头像二进制，并写入文件，保存每张头像；因为用户名是唯一的，所以根据uname获取头像
            f.write(img)


# 使用微信好友头像，根据输入的像素值大小，生成一张图片
def create_img():
    x = 0
    y = 0
    imgs = os.listdir("headImgs")  # 返回 headImgs 目录下的文件列表
    random.shuffle(imgs)  # 将文件列表随机排序

    input_length = int(input("请输入手机屏保长的像素值(一般是两个值中较大的值):"))
    input_width = int(input("请输入手机屏保宽的像素值(一般是两个值中较小的值):"))

    new_img = Image.new('RGBA', (input_width, input_length))  # 创建 长*宽 的图片用于填充各小图片
    width = int(math.sqrt(input_length * input_width / len(
        imgs)))  # 以 长*宽 来拼接图片，math.sqrt()开平方根计算每张小图片的宽高，这里设定每一张小图片还是正方形，虽然存在一点偏差，头像数量越多，壁纸右边和下边的空白越少
    num_line = int(input_width / width)  # 每行图片数

    for i in imgs:  # 对每一张图片逐个进行处理
        try:
            img = Image.open("headImgs/" + i)
        except IOError:
            print("第{}张图片为空".format(i))  # 可能会出现某张图片为空的情况
        else:
            img = img.resize((width, width), Image.ANTIALIAS)  # 缩小图片
            new_img.paste(img, (x * width, y * width))  # 拼接图片，一行排满，换行拼接
            x += 1
            if x >= num_line:
                x = 0
                y += 1

    new_img.save("mixedImg.png")
    itchat.send_image('mixedImg.png', toUserName='filehelper')  # 通过文件传输助手发送到自己微信中
    # newImg.show()


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)

    get_head_img(friends)
    create_img()

    # itchat.logout()
