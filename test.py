# coding=utf-8

import random
import re

import os
import requests
import sys
from PIL import Image,ImageEnhance
import pytesseract
import time
import json


tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
tessdata_dir = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

#192.168.20.246:8898
getCode='http://afilm.ezagoo.com/html/SecurityCode.aspx?mark='
verify='http://afilm.ezagoo.com/api/SendCode'
verify_url='http://afilm.ezagoo.com/api/SendCode?tel=%s&type=1&imgcode=%s'
rep={'O':'0', 'o':'0','C':'0',
    'I':'1','L':'1','q':'1',
    'Z':'2','z':'2',
    'S':'8','B':'8','b':'6',
     'T':'7','g':'8','Q':'0'
    };

# 随机生成手机号码
def createPhone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
               "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

 # 拼接url参数
def parse_url(data):
    item = data.items()
    urls = "?"
    for i in item:
        (key, value) = i
        temp_str = key + "=" + value
        urls = urls + temp_str + "&"
    urls = urls[:len(urls) - 1]
    return urls

def download_vcode(mobile):
    try:
        url = 'http://afilm.ezagoo.com/html/SecurityCode.aspx?mark=%s'%mobile
        #url='http://newoa.ezagoo.com/VCode.ashx'
        print (url)
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"'}
        s = requests.session()

        resp = s.get(url, headers=headers, verify=False)

        file_name = 'code.png'
        with open(file_name, 'wb') as f:
            f.write(resp.content)
    except Exception as e:
        print(e)

def verify_code(mobile,code):

    try:
        verify_parameter = {"tel": mobile,"type": "1","imgcode": code}
        #parse_url=verify + parse_url(verify_parameter)
        #parse_url = 'http://afilm.ezagoo.com/api/SendCode?tel={0}&type=1&imgcode={1}'.format(mobile,code)
        parse_url = verify_url % (mobile, code)
        print (parse_url)
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"'}
        s = requests.session()
        resp = s.get(parse_url, headers=headers, verify=False)
        type = sys.getfilesystemencoding()
        #print resp.status_code
        print (resp.content.decode('UTF-8'))
        #print('张俊'.encode('utf-8').decode('utf-8'))

        json_to_python = json.loads(resp.content)
        #print json_to_python['Code']
        global q
        if json_to_python['Code']=='101':
            path = "./pp/err_" + code + ".png"
            image = Image.open("code.png")
            image.save(path)
        elif json_to_python['Code']=='100':
            q += 1
        print (time.time())

    except Exception as e:
        print(e)

def initTable(threshold=140):           # 二值化函数
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def getsumdot(x, y, img):
    x = x - 1
    y = y - 1
    l1 = (x , y)
    l2 = (x + 1, y)
    l3 = (x + 2, y)
    m1 = (x , y + 1)
    m2 = (x + 1, y + 1)
    m3 = (x + 2, y + 1)
    b1 = (x , y + 2)
    b2 = (x + 1, y + 2)
    b3 = (x + 2, y + 2)
    sumdot = img.getpixel(l1) + img.getpixel(l2) + img.getpixel(l3) + \
        img.getpixel(m1) + img.getpixel(m2) + img.getpixel(m3) + \
        img.getpixel(b1) + img.getpixel(b2) + img.getpixel(b3)
    return sumdot

def removedot(img):
    x, y = img.size
    for ix in range(1, x-1):
        for iy in range(1, y-1):
            if img.getpixel((ix, iy)) == 0: # 0-black 1-white
                try:
                    sumdot = getsumdot(ix, iy, img)
                    if sumdot == 8:
                        # rmdot(ix,iy, img)
                        img.putpixel((ix, iy), 1)
                except Exception as e:
                    pass
    return img

def distinguish():
    print (time.time())
    str_phone=createPhone()
    download_vcode(str_phone)
    #识别图片
    image = Image.open("code.png")  # 打开验证码图片
    image.load()
    # image.show()
    # image.rotate(45).show() RGB  L

    im = image.convert('L')                                        #2.将彩色图像转化为灰度图

    binaryImage = im.point(initTable(), '1')                    #3.降噪，图片二值化
    #binaryImage.show()
    binaryImage = removedot(binaryImage)
    #binaryImage.show()

    text = pytesseract.image_to_string(binaryImage,config=tessdata_dir)

    print(text)

    text = re.sub("\W", "", text)
    for r in rep:
        text = text.replace(r,rep[r])
    if(len(text)==4):
        verify_code(str_phone,text)


if __name__ == "__main__":

    '''重命名文件
   
    for file in os.listdir("."):
        print file
        print os.path.splitext(file)[1]
        # if os.path.splitext(file)[1] == ".tmp":
        #     os.rename(file, os.path.splitext(file)[0] + ".jpg")
    '''
    distinguish()

    end=40000
    q=0
    count=True
    i_num=0
    # while (count):
    #     i_num+=1
    #     distinguish()
    #     time.sleep(1)
    #     print 'num:',i_num

    # for i in range(end):
    #     print i
    #     distinguish()
    #     time.sleep(1)
    #
    # print "识别了"+str(q)+"张验证码",'正确率为'+str((q/float(end))*100)+"%"

    #识别了2517张验证码 正确率为25.17%


