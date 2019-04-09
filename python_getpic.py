#coding=utf-8
import requests
import os

#此处路径自己修改，
path='D:\python_works\MyPython\png\\'
num=10
if os.path.exists(path):
    pass
else:
    os.makedirs(path)

for i in range(0,num):
    print("下载第"+str(i)+"张验证码")
    filePath=path+str(i)+'.gif'
    #这个地址下可以下载到普通的验证码
    r=requests.get('http://192.168.20.246:8898/html/SecurityCode.aspx?mark=17752855772')
    with open(filePath,'wb') as f:
        f.write(r.content)
