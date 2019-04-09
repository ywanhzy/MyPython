# -*- coding:utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from math import sqrt
import os
import re


def saveMod(num=50):
    '''
    获得大量切割后的验证码图片以获得模型
    '''
    nums = 0
    samples = os.listdir(path='.\简单验证码1')
    for sample in samples[:num]:
        im = Image.open(r'.\简单验证码1\%s' % sample)
        pieces = Div(im).imDiv()
        for img in pieces:
            nums += 1
            img.save(r'.\模板\%s.gif' % nums)


def getMods(Dir='模板'):
    '''
    读取模型图片
    为每个模型构建一个dict
    '''
    mods = {}
    # print('正在努力加载模型图片中...')
    print(os.getcwd())
    print(os.listdir(os.getcwd()))

    Mods = os.listdir('.\model')
    for Mod in Mods:

        name = re.findall(r'(.*?)\.gif', Mod)[0]
        # mods.setdefault(name, [])
        im = Image.open('model/'+Mod)
        mods[name] = getPoints(im)
    # print('模型加载完毕')
    return mods


def getPoints(im, captcha=0):
    """
    获取图片的像素点的坐标集合
    """
    pointSet = []
    frame = im.load()
    (w, h) = im.size
    for i in range(w):
        for j in range(h):
            if frame[i, j] == captcha:
                pointSet.append((i, j))
    return pointSet


class Div(object):

    """验证码图片分割"""

    def __init__(self, im):
        super(Div, self).__init__()
        self.im = im  # 原图，PIL.Image格式
        self.imgry = self.im.convert('L')  # 灰度图
        self.hist = self.im.convert('L').histogram()  # 灰度值
        self.imgPure = None  # 降噪后的二值化图
        self.starting = 0

    def _div(self, frame, w, h, captcha=0):
        '''
        从横坐标（w坐标）开始扫描，
        若找到验证码的在该坐标轴的开始的像素点，则做下标记
        最后返回所有验证码在坐标轴中的起始、结束四个坐标点
        '''
        pieces = []
        starting = 0
        ending = 256
        for i in range(w):
            for j in range(h):
                if frame[i, j] == captcha:
                    # 找到与背景灰度值不同的点，标记开始:self.starting = 1
                    # 横坐标的开始:i
                    if self.starting == 0:
                        self.starting = 1
                        starting = i
                    break
            if self.starting == 1:
                # 若已找到字符（self.starting == 1）且j已扫描至坐标的尽头（if j == (h-1)）
                # 说明字符已结束，记下ending
                if j == (h - 1):
                    self.starting = 0
                    ending = i
                    piece = [starting, 0, ending, h]
                    # 以上，完成x坐标（w坐标）起始点、结束点的扫描
                    # 接着扫描纵坐标
                    # 道理与上面完全相同，但是frame[i, j]的i、j应该颠倒位置，否则报错
                    for k in range(h):
                        for l in range(w):
                            if frame[l, k] == captcha:
                                if self.starting == 0:
                                    self.starting = 1
                                    starting = k
                                break
                        if self.starting == 1:
                            if l == (w - 1):
                                self.starting = 0
                                ending = k
                                piece[1] = starting
                                piece[3] = ending
                                pieces.append(piece)
        return pieces

    def showHist(self, w=512, h=512):
        '''
        将灰度直方图可视化展现出来
        '''
        histRaw = self.hist
        hist = [h - h * i / max(histRaw) for i in histRaw]  # 所有灰度值归一化处理
        w = w % 256 and 256 * (w / 256 + 1) or w  # 保证宽是256的倍数
        im2 = Image.new('L', (w, h), 255)
        draw = ImageDraw.Draw(im2)
        step = w / 256  # 每个矩形的宽度
        [draw.rectangle([i * step, hist[i], (i + 1) * step, h], fill=0)
         for i in range(256)]
        # im2.show()
        return im2

    def denoise(self):
        '''
        二值化处理
        根据该类验证码的特点进行定制化二值化处理
        '''
        table = []
        try:
            # 依据这组验证码的特点，取得上下门限阀值
            if self.hist[0] != 0:
                thresholdL = 0
                thresholdH = 2
            else:
                thresholdL = 253
                thresholdH = 255
            # 构造映射表进行映射、过滤去噪
            for i in range(256):
                if i >= thresholdL and i <= thresholdH:
                    table.append(0)
                else:
                    table.append(1)
            imgPure = self.imgry.point(table, '1')
            self.imgPure = imgPure
        except:
            print('去噪失败')
            pass

    def reDenoise(self, thresholdL=None, thresholdH=None):
        '''
        二值化处理，可取两个门限
        '''
        table = []
        try:
            if thresholdL is None or thresholdH is None:
                thresholdL = input('门限区间的较小值：\n')
                thresholdH = input('门限区间的较大值：\n')
            thresholdL = int(thresholdL)
            thresholdH = int(thresholdH)
            for i in range(256):
                if i >= thresholdL and i <= thresholdH:
                    table.append(0)
                else:
                    table.append(1)
            imgPure = self.imgry.point(table, '1')
            self.imgPure = imgPure
        except Exception as e:
            print(e)

    def imDiv(self, show=False):
        '''
        根据二值化、去噪后的图片进行分割图片
        返回类型：一个包含若干切好后的验证码的Image的列表
        '''
        imgPieces = []
        if self.imgPure is None:
            self.denoise()  # 默认使用自动降噪的方法
        if self.imgPure is None:
            print('未找到去噪后的图片')
            return None
        frame = self.imgPure.load()
        (w, h) = self.imgPure.size
        pieces = self._div(frame, w, h)
        for piece in pieces:
            im = self.imgPure.crop(piece)
            imgPieces.append(self.imgPure.crop(piece))
            if show is True:
                im.show()
        return imgPieces


class Recognize(object):

    """docstring for recognize"""

    def __init__(self):
        super(Recognize, self).__init__()
        self.mods = getMods()

    def var(self, sequence):
        '''
        计算数列的均方差
        同时进行归一化
        '''
        Sum = 0
        aver = sum(sequence) / len(sequence)
        for i in sequence:
            Sum += pow((i - aver), 2)
        deviation = sqrt(Sum / len(sequence))
        return 1 / (1 + deviation)

    def fitting(self, set1, set2):
        '''
        计算两个坐标点集合(即两张图的像素点)的相似度
        '''
        deviation = []
        lens = min(len(set1), len(set2))
        if lens > 0:
            for i in range(lens):
                dis = pow((set1[i][0] - set2[i][0]), 2) + \
                    pow((set1[i][1] - set2[i][1]), 2)
                deviation.append(dis)
                fitRate = self.var(deviation)
            return fitRate
        else:
            return 0

    def recognize(self, pieces):
        '''
        输入验证码碎片
        该函数依次将碎片与模型依次比较，找出最相似结果
        返回：一个含有结果的list
        '''
        results = []
        res = None
        for piece in pieces:
            fitMax = 0
            points = getPoints(piece)
            for mod in self.mods:
                rate = self.fitting(points, self.mods[mod])
                if rate > fitMax:
                    fitMax = rate
                    res = mod
            if res is not None:
                results.append(res)
        return results


def main():
   # img = input('请输入验证码图片名称\n(非同个文件夹下请输入包含路径的完整名称)\n')
    im = Image.open('captcha.jpeg')
    d = Div(im)
    r = Recognize()
    pieces = d.imDiv()
    res = r.recognize(pieces)
    print('识别结果是%s' % res)

if __name__ == "__main__":
    main()