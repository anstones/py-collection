#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
数字生成图片验证码
"""

import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage import transform as tf
# %matplotlib inline
from matplotlib import pyplot as plt


def create_captcha(text, shear=0, size=(100, 24),scale=1):

    # 我们使用字母L来生成一张黑白图像，为`ImageDraw`类初始化一个实例。这样，我们就可以用`PIL`绘图
    im = Image.new("L", size, "black")
    draw = ImageDraw.Draw(im)

    # 指定验证码文字所使用的字体。这里要用到字体文件，下面代码中的文件名（Coval.otf）应该指向文件存放位置（我把它放到当前笔记本所在目录）。
    font = ImageFont.truetype(r"Coval-Black.ttf", 22)
    draw.text((2, 2), text, fill=1, font=font)

    # 把PIL图像转换为`numpy`数组，以便用`scikit-image`库为图像添加错切变化效果。`scikit-image`大部分计算都使用`numpy`数组格式。
    image = np.array(im)

    affine_tf = tf.AffineTransform(shear=shear)
    image = tf.warp(image, affine_tf)

    # 最后一行代码对图像特征进行归一化处理，确保特征值落在0到1之间。归一化处理可在数据预处理、分类或其他阶段进行
    return image / image.max()

#
#生成验证码图像并显示它
image = create_captcha("GENE", shear=0.2)
plt.imshow(image, cmap='Greys')
