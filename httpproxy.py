__author__ = 'changchang.cc'
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import http.client
import threading
import time
from concurrent.futures import ThreadPoolExecutor

inFile = open('proxy.txt',encoding='utf-8')
outFile = open('verified.txt', 'w',encoding='utf-8')
lock = threading.Lock()

proxies = []
with open('verified_final.txt','r',encoding='utf-8') as f:
    l = f.readlines()
for i in l:
    data = {'http':'{}'.format(i.strip())}
    proxies.append(data)

def getpagethreading(targeturl="http://www.xicidaili.com/nn/",pages=10):
    tcount = 20
    n =11
    if pages % 10:
        tpages = pages//10+1
        flag = True
    else:
        tpages = pages//10
        flag = False
    if tpages < tcount:
        tcount = tpages
    all_thread = []
    for i in range(tcount):
        if i == tcount -1:
            if flag:
                n = pages%10+1
        t = threading.Thread(target=getProxyList,args=(targeturl,n,i,proxies[i]))
        all_thread.append(t)
        t.start()
        time.sleep(1)
    for t in all_thread:
        t.join()


def getProxyList(targeturl="http://www.xicidaili.com/nn/",last=11,n=0,proxies = None):
    countNum = 0
    last+=1

    proxyFile = open('proxy.txt' , 'a', encoding='utf-8')
    
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}

    for page in range(1, last):
        url = targeturl.format(page+n*10)
        req = requests.get(url, headers=requestHeader,proxies=proxies)
        # print(req.request.url)
        html_doc = req.text
    
        soup = BeautifulSoup(html_doc, "html.parser")
        # print(soup)
        trs = soup.find('tbody').find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            #国家
            if tds:
            #     nation = '未知'
            #     locate = '未知'
            # else:
            #     nation =   tds[0].find('img')['alt'].strip()
            #     locate  =   tds[3].text.strip()
                if targeturl==url2 or targeturl ==url3:
                    ip      =   tds[0].text.strip()
                    port    =   tds[1].text.strip()
                    anony   =   tds[2].text.strip()
                    protocol=   tds[3].text.strip()
                    locate  =   tds[4].text.strip()
                    speed   =   tds[5].text.strip()
                    t       =   tds[6].text.strip()
                elif targeturl==url1:
                    ip      = tds[0].text.strip()
                    port    = tds[1].text.strip()
                    anony   = tds[2].text.strip()
                    protocol= tds[3].text.strip()
                    locate  = tds[4].text.strip()
                    country = tds[5].text.strip()
                    company = tds[6].text.strip()
                    speed   = tds[7].text.strip()
                    lived   = tds[8].text.strip()
                    t       = tds[9].text.strip()

            
            proxyFile.write('%s|%s|%s|%s|%s|%s|%s\n' % (ip, port, anony, protocol, locate,speed, t) )
            print ('%s=%s:%s' % (protocol, ip, port))
            countNum += 1
        time.sleep(1)
    
    proxyFile.close()
    return countNum
    
def verifyProxyList(i):
    '''
    验证代理的有效性
    '''
    # requestHeader = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    # }
    requestHeader = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Cookie': 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1594807852,1595213110; historystock=600000%7C*%7C1A0001; spversion=20130314; v=AqKO_y05Cejz4xU0nu92WVvn8yMH86Y6WPeaMew6zpXAv0yV1IP2HSiH68K_',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
        'Host': 'q.10jqka.com.cn',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    myurl = 'http://q.10jqka.com.cn/index/'
    # print('读取位置：{}  线程id：{}'.format(inFile.tell(),i))

    while True:
        lock.acquire()
        # print('读取位置：{}  线程id：{}'.format(inFile.tell(), i))
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.split('|')
        protocol= line[3]
        ip      = line[0]
        port    = line[1]
        # for i in range(10):
        try:
            # conn = http.client.HTTPConnection(ip, port, timeout=3.0)
            # conn.request(method = 'GET', url = myurl, headers = requestHeader )
            # res = conn.getresponse()
            # print(res)
            # r = requests.get(myurl, headers = requestHeader, timeout = 3)
            r = requests.get(myurl, timeout=1, headers = requestHeader, proxies={'http': '{}://{}:{}'.format(protocol, ip, port)})
            soup = BeautifulSoup(r.content,'html.parser')
            # print(soup.find('title'))
            if soup.find('title').get_text() == '沪深市场_同花顺行情中心_同花顺财经网':#沪深市场_同花顺行情中心_同花顺财经网;百度一下，你就知道
                lock.acquire()
                print ("+++Success:" + ip + ":" + port)
                outFile.write( protocol.lower()+'://'+ip+':'+port+ "\n")
                lock.release()
            else:
                print("---Failure:" + ip + ":" + port)
        except Exception as e:
            print ("---Failure:" + ip + ":" + port)

    
if __name__ == '__main__':
    url1 = 'https://ip.jiangxianli.com/?page={}&anonymity=2'
    url2 = 'https://www.kuaidaili.com/free/inha/{}/'
    url3= 'https://www.kuaidaili.com/free/inha/{}/'

    tmp = open('proxy.txt' , 'w')
    tmp.write("")
    tmp.close()

    proxynum = getProxyList(url1,27)
    print (u"国内高匿：" + str(proxynum))
    # proxynum = getProxyList(url2,1000)
    # print (u"国内高匿：" + str(proxynum))
    # proxynum = getProxyList(url3,50)
    # print (u"国内透明：" + str(proxynum))
    # proxynum = getpagethreading(url2,10)
    # print (u"国内高匿：" + str(proxynum))
    # proxynum = getpagethreading(url3,10)
    # print (u"国内透明：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wn/")
    # print (u"国外高匿：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wt/")
    # print (u"国外透明：" + str(proxynum))



    print (u"\n验证代理的有效性：")

    # lentask = len(inFile.readlines())
    # p = [10,20,30,40,50,100]
    t = []
    # verifyProxyList(1)
    for i in range(10):
        # start = time.process_time()
        # print(start)
        tp = ThreadPoolExecutor(max_workers = 100)
        tp.map(verifyProxyList,[i for i in range(100)])
        # task1 = tp.submit(getProxyList)
        # print(task1.done)
        tp.shutdown()

        # t.append(end-start)
        inFile.seek(0)
    # for a in range(10):
    #     all_thread = []
    #     for i in range(5000):
    #         t = threading.Thread(target=verifyProxyList)
    #         all_thread.append(t)
    #         t.start()
    #
    #     for t in all_thread:
    #         t.join()
    #     inFile.seek(0)

    inFile.close()
    outFile.close()
    print ("All Done.")
    end = time.process_time()
    # print(end)
    # d = dict(zip(p,t))
    print('代码执行时长{}'.format(end))


