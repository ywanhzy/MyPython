#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *
import threading
import argparse


'''
端口检测
python  D:/python_works/MyPython/tcp.py -H 192.168.10.106

'''


lock = threading.Lock()
openNum = 0
threads = []

def portScanner(host,port):
    global openNum
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        lock.acquire()
        openNum+=1
        print('[+] %d open' % port)
        lock.release()
        s.close()
    except:
        pass

def main():
    p = argparse.ArgumentParser(description='Port scanner!.')
    p.add_argument('-H', dest='hosts', type=str)
    args = p.parse_args()
    hostList = args.hosts.split(',')
    setdefaulttimeout(1)
    for host in hostList:
        print('Scanning the host:%s......' % (host))
        for p in range(1,1024):
            #print p
            t = threading.Thread(target=portScanner,args=(host,p))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print('[*] The host:%s scan is complete!' % (host))
        print('[*] A total of %d open port ' % (openNum))

if __name__ == '__main__':
    main()



