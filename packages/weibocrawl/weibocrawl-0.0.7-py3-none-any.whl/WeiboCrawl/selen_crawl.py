# -*- coding:utf-8 -*-

import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from BaiduNews import info
from urllib import parse
import re
import json

import requests
import random


class Spider():

    def __init__(self, stamp=None):
        self.url = 'https://data.stats.gov.cn/search.htm?'
        self.stamp = (datetime.now()).strftime('%Y%m%d') if stamp is None else stamp
        self.client = MongoClient("localhost", 27017)
        # self.client = MongoClient("mongodb://other:nopassword@127.0.0.1/okooo")
        self.db=self.client['weibocrawl']
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()
        self.param={}
        self.urls = {}                      # 目标网页
        self.headers = {}                   # Get/Post请求头

    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls                                                  #http地址
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 发送Get请求
    def requests_get(self, url, data=None):
        try:
            url = url if data is None else url+parse.urlencode(data)
            print(url)
            # url = url.replace('%2C', ',').replace('%3A', ':').replace('%2B', '+')
            # if url in self.cachePool.keys():
            #     print('cache:')
            #     return self.cachePool[url]
            time.sleep(random.random() * 1 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            response = self.browser.get(url)
            value=self.browser.page_source


            # value = requests.get(url).text
            # value = requests.get(url, verify=False).text
            # print(value)
            # response = self.session.get(url, proxies=self.urls['proxies'], timeout=10)
            # response.encoding = 'utf-8'
            # value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            print(e)
            value = None
        finally:
            # pass
            return value
    # 保存htmlPage
    # 保存htmlPage
    def write_page(self, path, page):
        f = open(path, 'w')
        f.write(page.encode('utf-8'))
        f.close()
    # 保存htmlPage
    def read_page(self, path):
        with open(path,'r') as f:
            res=f.read()
            print(res)
            return f.read().decode('gbk')

    def headers_eval(self, headers):
        """
        headers 转换为字典
        :param headers: 要转换的 headers
        :return: 转换成为字典的 headers
        """
        try:
            headers = headers.splitlines()  # 将每行独立为一个字符串
            headers = [item.strip() for item in headers if item.strip() and ":" in item]  # 去掉多余的信息 , 比如空行 , 非请求头内容
            headers = [item.split(':') for item in headers]  # 将 key value 分离
            headers = [[item.strip() for item in items] for items in headers]  # 去掉两边的空格
            headers = {items[0]: items[1] for items in headers}  # 粘合为字典
            headers = json.dumps(headers, indent=4, ensure_ascii=False)  # 将这个字典转换为 json 格式 , 主要是输出整齐一点
            print(headers)
        except Exception:
            print("headers eval get error ...")
            headers = dict()

        return headers

    def headers_get(self, get_headers):
        """
        headers 转换为字典
        :param headers: 要转换的 headers
        :return: 转换成为字典的 headers
        """
        try:
            get0=get_headers.split('?')[0]
            print(get0)
            get1 = get_headers.split('?')[1]
            headers = get1.replace('=',':')
            headers = headers.split('&')  # 将每行独立为一个字符串
            headers = [item.strip() for item in headers if item.strip() and ":" in item]  # 去掉多余的信息 , 比如空行 , 非请求头内容
            headers = [item.split(':') for item in headers]  # 将 key value 分离
            headers = [[item.strip() for item in items] for items in headers]  # 去掉两边的空格
            headers = {items[0]: items[1] for items in headers}  # 粘合为字典
            headers = json.dumps(headers, indent=4, ensure_ascii=False)  # 将这个字典转换为 json 格式 , 主要是输出整齐一点
            print(headers)
        except Exception:
            print("headers eval get error ...")
            headers = dict()

        return headers

    # 下载数据并保存
    def pb_repair(self):
        self._matches = self.db['renwumag1980_2']
        try:
            # 不为空查询
            matches = self._matches.find({'is_original': '转载'})
            # matches = self._matches.find({'video_num': {'$gte': 1}})
            for match in matches:
                try:
                    # content_url=match['content_url']
                    # arc_html = self.requests_get(content_url)
                    # match['arc_html']=arc_html

                    if match['key3'] is not None:
                        continue

                    arc_html=match['arc_html']

                    try:
                        # arc_html=match['arc_html']
                        # print(arc_html)
                        # soup_body = BeautifulSoup(arc_html, "html.parser")
                        print('解析')
                        print(match['content_url'])

                        rex = r'来源 \|(.*?)（ID:.*'

                        pos=arc_html.find('来源 |')
                        pos_str=arc_html[pos:pos+200]
                        # print(pos_str)

                        matchObj = re.match(rex, pos_str, re.M | re.I)
                        if matchObj:
                            rex_src=matchObj.group(1).strip().split(';')[-1]
                            match['key3']=rex_src
                            print(rex_src)
                    except:
                        pass


                    self._matches.update_one({'symbol': match['symbol']}, {"$set": match}, True)
                except Exception as e:
                    print(e)
                    continue
            print(matches.count())
        except:
            print (self.stamp + " error, quit()")
            quit()

    def Imatate(self):
        self.update_info()
        # self._matches = self.db['renwumag1980_2']

        # page=requests.get('https://www.amazon.com/Finer-Things-Timeless-Furniture-Textiles/dp/0770434290/ref=lp_4539344011_1_1?s=books&ie=UTF8&qid=1605336684&sr=1-1').text
        # print(page)
        # return

        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
        # chrome_options.add_argument('--headless')
        # selenium 运行时会从系统的环境变量中查找 webdriver.exe
        # 一般把 webdriver.exe 放到 python 目录中，这样就不用在代码中指定。
        chrome_driver = "C:\Program Files\Google\Chrome\Application/chromedriver.exe"
        self.browser = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

        cookie={
            "rewardsn":"",
            "wxtokenkey": "777",
        }

        # self.browser.add_cookie({'rewardsn':'','wxtokenkey':'777'})

        self.browser.add_cookie({'name': 'ASP.NET_SessionId', 'value': 'yy3mnikt0zqeolotjahrrkte'})
        self.browser.add_cookie({'name': 'fvlid', 'value': '1605284317709aRf8bjOAb0'})

        self.browser.get("https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4554976677862363&from=singleWeiBo&__rnd=1606148096743")
        # print(self.browser.page_source)

        soup=BeautifulSoup(self.browser.page_source, 'lxml')
        data=json.loads(soup.text)
        print(data['data'])

        return

        # self.browser = webdriver.PhantomJS()
        # self.browser.implicitly_wait(10)  # 这里设置智能等待10s

        # url = 'https://linwanwan668.taobao.com/i/asynSearch.htm?mid=w-553869820-0&orderType=hotsell_desc'
        url='https://sycm.taobao.com/portal/home.htm?spm=a211vu.server-home.category.d780.4c575e16BTnoaM'


        try:
            # self.crawl3(url)
            self.pb_repair()
        finally:
            # self.browser.close()
            self.client.close()

    # 解析数据
    def export(self):
        try:
            # for record in self._records.find():
            #     self.parse(record['result'])
            #     for betfair in record['betfair']:
            #         self.parse2(betfair)
            page=self.read_page('test.txt')
            print(page)
        except:
            pass

if __name__ == '__main__':

    hear='''
    
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Cookie: SINAGLOBAL=5579701838206.736.1605880029171; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWgxyR8DlA5uOfXLUFsnVlP5JpX5KMhUgL.FoeXS0.NeoqN1KM2dJLoI7_DMcHfSoqcP0zEe5tt; wvr=6; ALF=1638440600; SSOLoginState=1606904602; SCF=Alx6A-qiJFwbh6ziknk_s1AyMls2FBOF9t8ivMLmXxCSv-cV1u5A5MvQ7e5wGCAzTMo6mU973O8Vpaxr1vMYMwY.; SUB=_2A25ywxtKDeRhGeVK7FsW8ijLwjuIHXVRuQuCrDV8PUNbmtAfLRPZkW9NTCmebnHFYruX_eYSLN_EHgYLziZ0Xe-Y; _s_tentry=www.baidu.com; UOR=login.sina.com.cn,weibo.com,www.baidu.com; Apache=2348076874160.583.1606904618773; ULV=1606904618796:11:2:3:2348076874160.583.1606904618773:1606883523356; webim_unReadCount=%7B%22time%22%3A1606906165777%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A45%2C%22msgbox%22%3A0%7D; WBStorage=8daec78e6a891122|undefined
Host: s.weibo.com
Referer: https://s.weibo.com/weibo?q=%E9%B2%8D%E6%AF%93%E6%98%8E%E6%B6%89%E5%AB%8C%E6%80%A7%E4%BE%B5%E5%85%BB%E5%A5%B3&Refer=index
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52
    '''

    spider=Spider()
    # spider.Imatate()
    # spider.pb_repair()

    # spider.headers_get(hear)
    spider.headers_eval(hear)


    print(datetime.now())
