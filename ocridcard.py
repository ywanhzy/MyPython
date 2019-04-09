# coding=utf-8
import requests
from json import JSONDecoder
import os

from PIL import Image


def download_vcode():
    try:
        url = 'http://newoa.ezagoo.com/VCode.ashx'
        #url='http://newoa.ezagoo.com/VCode.ashx'
        print url
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"'}
        s = requests.session()

        resp = s.get(url, headers=headers, verify=False)

        file_name = 'code.jpg'
        with open(file_name, 'wb') as f:
            f.write(resp.content)
    except Exception as e:
        print(e)

# download_vcode()


def ResizeImage(filein, fileout, width, height, type):
  img = Image.open(filein)
  assert isinstance(img,Image.Image)
  img = img.convert('RGB')
  out = img.resize((width, height),Image.ANTIALIAS) #resize image with high-quality
  out.save(fileout)


# filein = r'code.jpg'
# fileout = r'code1.jpg'
# width = 70
# height = 48
# type = 'jpg'
#
# ResizeImage(filein, fileout, width, height, type)


#http_url = "https://api-cn.faceplusplus.com/imagepp/beta/recognizetext" #文字识别
http_url = "https://api-cn.faceplusplus.com/cardpp/v1/ocridcard" #身份证识别

key = "YV1vEA-78ceykcBBfLHopPlVgTHCIAn0"
secret = "_LEgobcN6t4oVaqkqUxUFjRgwu1lU8lw"

data = {"api_key": key, "api_secret": secret, "legality": "1"}
#data = {"api_key": key, "api_secret": secret}
files = {"image_file": open("IMG_0446.jpg", "rb")}
response = requests.post(http_url, data=data, files=files)

req_con = response.content.decode('unicode_escape')

req_dict = JSONDecoder().decode(req_con)
print (req_con)
# print (req_dict)