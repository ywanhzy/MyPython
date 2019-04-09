# coding=utf-8

# 由于MD5模块在python3中被移除
# 在python3中使用hashlib模块进行md5操作
import hashlib
import json

import time
import sched
from imp import reload
from threading import Timer

import datetime
import requests
import sys

from Email import sendEmail

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# 待加密信息
# str = 'ae9a8ccd-e8ff-4586-9d50-0497fb15772fezgsign'

# value：ae9a8ccd-e8ff-4586-9d50-0497fb15772fezgsign
# md5Value：8bb3b187bdf380d59ae03a70e1001d65

# 生成MD5
def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))
    print('MD5加密前为 ：' + str)
    print('MD5加密后为 ：' + hl.hexdigest())
    return hl.hexdigest()

# genearteMD5(str)
def doSth():
    print('test')
    # 假装做这件事情需要一分钟
    time.sleep(60)

def main(h=9, m=24):
    '''h表示设定的小时，m为设定的分钟'''
    print ("sdfds")
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            print (now.hour)
            # 到达设定时间，结束内循环
            if now.hour == h and now.minute == m:
                print ("成功")
                time.sleep(60)
                break  # 不到时间就等20秒之后再次检测
            time.sleep(10)
        # 做正事，一天做一次
        doSth()

# main()


#
#  token	是	登录令牌
# string gpsx	是	经度
# string gpsy	是	纬度
# string addrstate	是	办公区域名称
# string signaddress	是	详细地址
# string imei
def signin_oa(token):
    signencrypt=genearteMD5(token+'ezgsign')
    url = 'http://192.168.1.222:5112/sign/signsave.ashx'
    d = {'token': token, 'gpsx': '112.72589','gpsy':'28.236564','addrstate':'光明村','signaddress':'湖南省长沙市望城区473乡道88号靠近青竹塘','imei':'865763038685720','signencrypt':signencrypt,'remark':'isEmulator:false'}
    print (d)
    r = requests.post(url, data=d)
    data = json.loads(r.text)
    print (type(d))
    rs=json.dumps(d).decode('unicode-escape')
    print (str(rs))
    sendEmail(data.get('action'),str(rs))
    print (r.text)


# string account	是	账号
# string pwd	是	密码
# string type	否	系统类型 1ios   2android  3web
# string version	否	系统版本 如 iphone5 9.3.1   android 4.3.1
# string regid	是	极光注册id
def login_oa():
    url = 'http://192.168.1.222:5112/login.ashx'
    d = {'account': '刘牧', 'pwd': '111111','type':'2','version':'','regid':''}
    print (d)
    r = requests.post(url, data=d)
    data = json.loads(r.text)
    print (data)
    #json两种取值方式
    print (data['plusData']['userdata']['token'])
    print (data.get('plusData').get('userdata').get('token'))
    token=data['plusData']['userdata']['token']
    signin_oa(token)

    print (r.text)

login_oa()

def get_news():
    # 这里是把今日糍粑每日一句中拿过来的信息发送给你朋友
    url = "http://open.iciba.com/dsapi/"

    r = requests.get(url)
    contents = r.json()['content']
    translation = r.json()['translation']
    return contents, translation


# print (get_news()[0])
# print (get_news()[1][5:])




# genearteMD5(str)

def func(msg, starttime):
    print (u'程序启动时刻：', starttime, '当前时刻：', time.time(), '消息内容 --> %s' % (msg))


# 下面的两个语句和上面的 scheduler 效果一样的
Timer(5, func, ('hello', time.time())).start()
Timer(3, func, ('world', time.time())).start()

count = 0


def loopfunc(msg, starttime):
    global count
    print (u'启动时刻：', starttime, ' 当前时刻：', time.time(), '消息 --> %s' % (msg))
    count += 1
    if count < 30000:
        Timer(3, loopfunc, ('world %d' % (count), time.time())).start()


# Timer(3, loopfunc, ('world %d' % (count), time.time())).start()



# 第一个工作函数
# 第二个参数 @starttime 表示任务开始的时间
# 很明显参数在建立这个任务的时候就已经传递过去了，至于任务何时开始执行就由调度器决定了
def worker(msg, starttime):
    print (u"任务执行的时刻", time.time(), "传达的消息是", msg, '任务建立时刻', starttime)


    # # 创建一个调度器示例
    # # 第一参数是获取时间的函数，第二个参数是延时函数
    # print u'----------  两个简单的例子  -------------'
    # print u'程序启动时刻：', time.time()
    # s = sched.scheduler(time.time, time.sleep)
    # s.enter(1, 1, worker, ('hello', time.time()))
    # s.enter(3, 1, worker, ('world', time.time()))
    # s.run()  # 这一个 s.run() 启动上面的两个任务
    # print u'睡眠２秒前时刻：', time.time()
    # time.sleep(2)
    # print u'睡眠２秒结束时刻：', time.time()


    # 　重点关注下面２个任务，建立时间，启动时间
    # ２个任务的建立时间都很好计算，但有没有发现 "hello world [3]"　的启动时间比建立时间晚　１３　秒，
    # 这不就是２个 sleep　的总延时吗？所以说启动时间并不一定就是 delay　能指定的，还需要看具体的程序环境，
    # 如果程序堵塞的很厉害，已经浪费了一大段的时间还没有到 scheduler 能调度这个任务，当 scheduler 能调度这个
    # 任务的时候，发现 delay 已经过去了， scheduler 为了弥补“罪过”，会马上启动这个任务。

    # 任务 "hello world [15]" 就是一个很好的例子，正常情况下，程序没有阻塞的那么厉害，在scheduler　能调度这个任务的时候
    # 发现 delay 还没到就等待，如果 delay　时间到了就可以在恰好指定的延时调用这个任务。
    # print u'\n\n----------  两个复杂的例子  -------------'
    # s.enter(3, 1, worker, ('hello world [3]', time.time()))
    # print u'睡眠７秒前时刻：', time.time()
    # time.sleep(7)
    # print u'睡眠７秒结束时刻：', time.time()
    #
    # s.enter(15, 1, worker, ('hello world [15]', time.time()))
    # print u'睡眠６秒前时刻：', time.time()
    # time.sleep(6)
    # print u'睡眠６秒结束时刻：', time.time()
    #
    # s.run() # 过了2秒之后，启动另外一个任务
    #
    #
    # print u'程序结束时刻', time.time()

    ##################################################333333

    # # 计数器，一个循环任务，总共让自己执行3次
    # total = 0
    # # 第二个工作函数，自调任务，自己开启定时并启动。
    # def worker2(msg, starttime):
    #     global total
    #     total += 1
    #     print u'当前时刻：', time.time(), '消息是：', msg, ' 启动时间是：', starttime
    #     # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    #     if total < 3:
    #         # 这里的delay 可以重新指定
    #         s.enter(5, 2, worker2, ('perfect world %d' % (total), time.time()))
    #         s.run()
    #
    # print u'程序开始时刻：', time.time()
    # # 开启自调任务
    # s.enter(5, 2, worker2, ('perfect world %d' % (total), time.time()))
    # s.run()
    # print u'程序结束时刻：', time.time()
