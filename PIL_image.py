#coding=utf-8
from PIL import Image, ImageDraw,ImageFont
import matplotlib.pyplot as plt
import numpy as np
from pylab import *

'''
matplotlib.pyplot.figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None)
所有参数都是可选的，都有默认值，因此调用该函数时可以不带任何参数，其中：
num: 整型或字符型都可以。如果设置为整型，则该整型数字表示窗口的序号。如果设置为字符型，则该字符串表示窗口的名称。用该参数来命名窗口，如果两个窗口序号或名相同，则后一个窗口会覆盖前一个窗口。
figsize: 设置窗口大小。是一个tuple型的整数，如figsize=（8，8）
dpi: 整形数字，表示窗口的分辨率。
facecolor: 窗口的背景颜色。
edgecolor: 窗口的边框颜色。
用figure()函数创建的窗口，只能显示一幅图片，如果想要显示多幅图片，则需要将这个窗口再划分为几个子图，在每个子图中显示不同的图片。我们可以使用subplot（）函数来划分子图，函数格式为：
matplotlib.pyplot.subplot(nrows, ncols, plot_number)
nrows: 子图的行数。
ncols: 子图的列数。
plot_number: 当前子图的编号。

'''

# img=Image.open('IMG_0446.jpg')  #打开图像

# img = img.resize((1224, 1600))
# img = img.rotate(90) # 顺时针角度表示
# plt.figure("title")
#plt.figure(num='astronaut',figsize=(8,8))
#plt.axis('on')#不显示坐标尺寸

# gray=img.convert('L')   #转换成灰度
# r,g,b=img.split()   #分离三通道
# print  r,g,b
# pic=Image.merge('RGB',(r,g,b)) #合并三通道
#
# plt.subplot(2,3,1), plt.title('origin')
# plt.imshow(img),plt.axis('off')
# plt.subplot(2,3,2), plt.title('gray')
# plt.imshow(img,cmap='gray'),plt.axis('off')
# plt.subplot(2,3,3), plt.title('merge')
# plt.imshow(pic),plt.axis('off')
# # plt.subplot(2,3,5), plt.title('g')
# # plt.imshow(g,cmap='gray'),plt.axis('off')
# # plt.subplot(2,3,6), plt.title('b')
# # plt.imshow(b,cmap='gray'),plt.axis('off')
# plt.show()


#画图
# draw = ImageDraw.Draw(img)
# draw.text((160, 160), "东方闪电双方的发生", (255, 0, 0), font=font)    #设置文字位置/内容/颜色/字体
# draw = ImageDraw.Draw(img)                          #Just draw it!
#
# #另存图片
# img.show()

font = ImageFont.truetype("C:\Windows\Fonts\simkai.ttf", 34)

# image: 图片  text：要添加的文本 font：字体
def add_text_to_image(image, text, font=font):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    print(rgba_image)
    text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)
    print text_xy
    # 设置文本颜色和透明度
    image_draw.text(text_xy, unicode(text,'utf-8'), font=font, fill=(76, 234, 124,255))
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_text
img=Image.open('IMG_0446.jpg')  #打开图像
# im_before = Image.open("lena.jpg")
# img.show()
im_after = add_text_to_image(img, 'dsfdsd')
im_after.show()

'''
'''
# X = [[1, 2], [3, 4]]
# fig = plt.figure()
# ax = fig.add_subplot(231)
# ax.imshow(X)
# ax = fig.add_subplot(232)
# ax.imshow(X, cmap=plt.cm.gray)  # 灰度
# ax = fig.add_subplot(233)
# im = ax.imshow(X, cmap=plt.cm.spring)  # 春
# plt.colorbar(im)
# ax = fig.add_subplot(234)
# im = ax.imshow(X, cmap=plt.cm.summer)
# plt.colorbar(im, cax=None, ax=None, shrink=0.5)  # 长度为半
# ax = fig.add_subplot(235)
# im = ax.imshow(X, cmap=plt.cm.autumn)
# plt.colorbar(im, shrink=0.5, ticks=[-1, 0, 1])
# ax = fig.add_subplot(236)
# im = ax.imshow(X, cmap=plt.cm.winter)
# plt.colorbar(im, shrink=0.5)
# plt.show()
'''
'''

# img = np.array(img)
# if img.ndim == 3:
#     img = img[:,:,0]
# plt.subplot(221), plt.imshow(img)
# plt.subplot(222), plt.imshow(img, cmap ='gray')
# plt.subplot(223), plt.imshow(img, cmap = plt.cm.gray)
# plt.subplot(224), plt.imshow(img, cmap = plt.cm.gray_r)
# plt.show()


#img = img.transpose(Image.FLIP_LEFT_RIGHT) #左右互换
#img = img.transpose(Image.FLIP_TOP_BOTTOM) #上下互换
#img = img.transpose(Image.ROTATE_90)  #顺时针旋转
# img = img.transpose(Image.ROTATE_180)
# img = img.transpose(Image.ROTATE_270)
# img.show()


# plt.subplot(2,1,1), plt.title('origin')
# plt.imshow(img),plt.axis('off')

#plt.subplot(231)
# plt.plot([1,2,3])

# box=(780,400,1200,1100)
# img=img.crop(box)
# plt.subplot(1,1,1), plt.title('截取')
# plt.imshow(img),plt.axis('off')

# plt.show()


'''
绘制各类2d图形
'''
# x = [1, 2, 3, 4]
# y = [3, 5, 10, 25]
#
# # 创建Figure
# fig = plt.figure()
#
# # 创建一个或多个子图(subplot绘图区才能绘图)
# ax1 = fig.add_subplot(231)
# plt.plot(x, y, marker='o')  # 表示绘制折线图 marker设置样式菱形 绘图及选择子图
# plt.sca(ax1)
#
# ax2 = fig.add_subplot(232)
# plt.scatter(x, y, marker='s', color='r') # 绘制散点图，红色正方形
# plt.sca(ax2)
# plt.grid(True)
#
# ax3 = fig.add_subplot(233)
# plt.bar(x, y, 0.5, color='c')  #  绘制柱状图，间距为0.5，原色
# plt.sca(ax3)
#
# ax4 = fig.add_subplot(234)
# # 高斯分布
# mean = 0  # 均值为0
# sigma = 1  # 标准差为1 (反应数据集中还是分散的值)
# data = mean + sigma * np.random.randn(10000)
# plt.hist(data, 40, normed=1, histtype='bar', facecolor='yellowgreen', alpha=0.75) #直方图
# plt.sca(ax4)
#
# m = np.arange(-5.0, 5.0, 0.02)
# n = np.sin(m)
# ax5 = fig.add_subplot(235)
# plt.plot(m, n)
# plt.sca(ax5)
#
# ax6 = fig.add_subplot(236)
# xlim(-2.5, 2.5)  # 设置x轴范围
# ylim(-1, 1)  # 设置y轴范围
# plt.plot(m, n)
# plt.sca(ax6)
# plt.grid(True)
#
# plt.show()


# def add_watermark_to_image(image, watermark):
#     rgba_image = image.convert('RGBA')
#     rgba_watermark = watermark.convert('RGBA')
#
#     image_x, image_y = rgba_image.size
#     watermark_x, watermark_y = rgba_watermark.size
#
#     # 缩放图片
#     scale = 10
#     watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
#     new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
#     rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
#     # 透明度
#     rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 180))
#     rgba_watermark.putalpha(rgba_watermark_mask)
#
#     watermark_x, watermark_y = rgba_watermark.size
#     # 水印位置
#     rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask)
#
#     return rgba_image
#
# im_before = Image.open("IMG_0446.jpg")
# im_before.show()
#
# im_watermark = Image.open("code.jpg")
# im_after = add_watermark_to_image(im_before, im_watermark)
# im_after.show()
# im.save('im_after.jpg')