# -*- coding:utf-8 -*-

# __author:ly_peppa
# date:2020/11/24


# 0.0.1更新：googlenews改为baidunews


import sys
import re
import json
import math
import requests
from bs4 import BeautifulSoup
from WeiboCrawl import info
from collections import OrderedDict
from datetime import datetime
import time
import random
import datetime
from urllib import parse
import pandas as pd


requests.packages.urllib3.disable_warnings()


class WeiboCrawl():

    def __init__(self):
        self.author_wx = 'ly_peppa'
        self.author_qq = '3079886558'
        self.author_email = 'iseu1130@sina.cn'
        self.urls = {}                      # 目标网页
        self.headers = {}                   # Get/Post请求头
        self.param = {}
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()
        self.keyword=None
        self.df_keyword=None
        self.df_topic = None
        self.df_comment=None
        self.df_retweet = None
        self.df_weibo=None
        self.df_info = pd.DataFrame(columns=['user_id', 'user_name', 'gender', 'birthday', 'location', 'education', 'company', 'registration_time', 'sunshine', 'statuses_count', 'followers_count', 'follow_count', 'description', 'profile_url', 'profile_image_url', 'avatar_hd', 'urank', 'mbrank', 'verified', 'verified_type', 'verified_reason'])
        self.user={'user_name':'user_name',
                   'user_id':'user_id',}

    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls                                                  #http地址
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 发送Get请求
    def requests_get(self, url, data=None, headers=None):
        try:
            url = url if data is None else url+parse.urlencode(data)
            time.sleep(random.random() * 3 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            print(json.dumps(self.urls['proxies']) + ' --> ' + url)
            # response = self.session.get(url, proxies=self.proxy, headers=headers, verify=False)
            # self.session.keep_alive = False
            # response = requests.get(url, headers=headers, proxies=self.proxy, timeout=10, verify=False)
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            # response.encoding = response.apparent_encoding
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value

    # 搜索关键字
    def search_keywords(self, keyword, day=-365 * 50, pn=None):
        self.keyword = keyword
        result = None
        try:
            self.df_keyword = pd.DataFrame(
                columns=["mid", "user_id", "user_name",  "user_verify",  "user_hot",  "comment", "topic_url", "img_urls",  "wb_time",  "source", "comment_count", "retweet_count", "like_count"])
            self.param['keyword']['page'] = 0
            # 翻页
            # self.keyword_next(keyword, day=day, pn=pn)
            for index in range(1, pn + 1):
                self.keyword_next(keyword, day=day, pn=pn)

            result = self.df_keyword

        except Exception as e:
            print(e)
        finally:
            return result

    # 评论翻页
    def keyword_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['keyword']['page']>=pn:
                    return result
                if self.param['keyword']['page']>100:
                    return result
            self.param['keyword']['page'] = self.param['keyword']['page'] + 1
            if keyword.startswith('http'):
                response = self.requests_get(keyword, headers=self.headers['weibo'])
            else:
                response = self.requests_get(self.urls['keyword'], data=self.param['keyword'], headers=self.headers['weibo'])
            # print(response.text)
            if response is None:
                return result
            # self.keyword_parse(response.text, flag='kw')

            inner=self.keyword_parse(response.text, flag='kw')
            # while inner is not None:
            #     try:
            #         next_url = 'https://s.weibo.com' + inner['href']
            #         inner = self.keyword_next(next_url, pn=pn)
            #     except:
            #         pass
            result=self.df_keyword

        except Exception as e:
            print(e)
        finally:
            return result

    # 评论翻页
    def keyword_parse(self, web_content, flag='kw'):
        result=None
        try:
            soup = BeautifulSoup(web_content, 'lxml')
            feedlist = soup.find('div', id='pl_feedlist_index')
            list_item = feedlist.find_all('div', attrs={'class': re.compile("card-wrap"),
                                                            'action-type': re.compile("feed_list_item")})
            page_inner = soup.find('a', text='下一页')
            for root in list_item:
                try:
                    mid = root['mid']
                    # print('名称id')
                    # info = root.find('div', class_='info').find('a', attrs={'href': re.compile("//weibo.com")})
                    info = root.find('div', class_='info').find_all('a')
                    user_name=info[2]['nick-name']
                    user_href="https:"+info[2]['href']
                    user_id = user_href.split('?')[0].split('/')[-1]
                    verify=None
                    if len(info)>3:
                        verify=info[3]['title'].strip()
                    # print('内容')
                    list_content = root.find('p', attrs={'class': re.compile("txt"), 'node-type': re.compile("feed_list_content")})
                    content=list_content.text.strip()
                    p_href=None
                    try:
                        p_href = list_content.a['href']
                        p_href = p_href if p_href.startswith('https') else None
                    except:
                        pass

                    # a_href = list_content[-1]['href']
                    # print('图片')
                    media_prev = root.find('div', attrs={'node-type': re.compile("feed_list_media_prev")})
                    img_urls=[]
                    if media_prev:
                        imgs=media_prev.find_all('img', attrs={'action-type': re.compile("fl_pics")})
                        for img in imgs:
                            img_urls.append("https:"+img['src'])
                    img_urls = None if img_urls == [] else img_urls
                    pfrom = root.find('p', class_='from')
                    wb_time=pfrom.a.text.split('转赞')[0].strip()
                    # wb_from=pfrom.text.split('来自')[-1].strip()
                    # wb_from=None if wb_from==wb_time else wb_from
                    wb_from=None
                    laizi= pfrom.text.split('来自')
                    if len(laizi)>1:
                        wb_from=laizi[1].strip()


                    # print('评论转发')
                    cardact = root.find('div', class_='card-act')
                    lis = cardact.find_all('li')
                    zhuanfa = None
                    pinglun = None
                    dianzan = None
                    if lis:
                        zhuanfa = lis[1].text.replace('转发 ', '').strip()
                        pinglun = lis[2].text.replace('评论 ', '').strip()
                        dianzan = lis[3].text.strip()
                        zhuanfa = '0' if zhuanfa =='' else zhuanfa
                        pinglun = '0' if pinglun == '' else pinglun
                        dianzan = '0' if dianzan == '' else dianzan

                    row=[mid, user_id, user_name, verify,  user_href, content, p_href, img_urls, wb_time, wb_from, zhuanfa, pinglun, dianzan]
                    print(row)
                    if flag=='kw':
                        self.df_keyword.loc[len(self.df_keyword)] = row
                    elif flag == 'tp':
                        self.df_topic.loc[len(self.df_topic)] = row
                except Exception as e:
                    print(e)
                    pass

            # if flag == 'kw':
            #     result=self.df_keyword
            # elif flag == 'tp':
            #     result=self.df_topic
            result=page_inner
        except Exception as e:
            print(e)
        finally:
            return result

    # 搜索话题
    def search_topics(self, keyword, day=-365 * 50, pn=None):
        self.keyword = keyword
        result = None
        try:
            self.df_topic = pd.DataFrame(
                columns=["mid", "user_id", "user_name",  "user_verify", "user_hot",  "comment", "topic_url", "img_urls",  "wb_time",  "source", "comment_count", "retweet_count", "like_count"])
            self.param['topic']['page'] = 0
            # 翻页
            # self.topic_next(keyword, day=day, pn=pn)
            for index in range(1, pn + 1):
                self.topic_next(keyword, day=day, pn=pn)

            result = self.df_topic

        except Exception as e:
            print(e)
        finally:
            return result

    # 评论翻页
    def topic_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['topic']['page']>=pn:
                    return result
                if self.param['topic']['page']>100:
                    return result
            self.param['topic']['page'] = self.param['topic']['page'] + 1
            if keyword.startswith('http'):
                response = self.requests_get(keyword, headers=self.headers['weibo'])
            else:
                response = self.requests_get(self.urls['topic'], data=self.param['topic'], headers=self.headers['weibo'])
            # print(response.text)
            if response is None:
                return result
            inner=self.keyword_parse(response.text, flag='tp')
            # if inner is not None:
            #     next_url = 'https://s.weibo.com' + inner['href']
            #     self.topic_next(next_url, pn=pn)

            result=self.df_topic

        except Exception as e:
            print(e)
        finally:
            return result


    # 搜索评论
    def search_comments(self, keyword, day=-365*50, pn=None):
        self.keyword = keyword
        result=None
        try:
            self.df_comment = pd.DataFrame(columns=["mid", "user_id", "user_name", "comment", "comment_time", "like_count"])
            self.param['comment']['id'] = keyword
            self.param['comment']['page'] = 0
            # 翻页
            for index in range(1, pn+1):
                self.comment_next(keyword, day=day, pn=pn)

            result=self.df_comment

        except Exception as e:
            print(e)
        finally:
            return result

    # 评论翻页
    def comment_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['comment']['page']>=pn:
                    return result
                if self.param['comment']['page']>100:
                    return result
            # self.param['comment']['id'] = keywords
            self.param['comment']['page'] = self.param['comment']['page'] + 1
            response = self.requests_get(self.urls['comment'], data=self.param['comment'], headers=self.headers['home'])
            # print(response.text)
            if response is None:
                return result
            web_content = json.loads(response.text)['data']['html']
            soup = BeautifulSoup(web_content, 'lxml')
            page_inner = soup.find('span', class_='more_txt')
            list_box = soup.find('div', class_='list_box')
            root_comments = list_box.find_all('div', attrs={'class': re.compile("list_li S_line1 clearfix"),
                                                            'node-type': re.compile("root_comment")})
            for root in root_comments:
                try:
                    WB_text = root.find('div', class_='WB_text')
                    user_id = WB_text.a['usercard'].split('=')[-1].strip()
                    user_name = WB_text.a.text.strip()
                    content = WB_text.text.split('：')[-1].strip()
                    WB_from = root.find('div', class_='WB_from S_txt2')
                    user_time = WB_from.text.strip()
                    WB_handle = root.find('div', class_='WB_handle W_fr')
                    lis = WB_handle.find_all('li')
                    li1 = None
                    # li2 = None
                    if lis:
                        li1 = lis[-1].text.replace('ñ', '').replace('赞', '0').strip()
                        # li2 = lis[-2].text.strip()

                    row = [keyword, user_id, user_name, content, user_time, li1]
                    # # 时间筛选
                    # try:
                    #     news_date = datetime.datetime.strptime(news_stamp, "%Y年%m月%d日 %H:%M")
                    #     now = datetime.datetime.now()
                    #     delta = datetime.timedelta(days=day)
                    #     pre_date = now + delta
                    #     if news_date < pre_date:
                    #         continue
                    # except:
                    #     news_stamp = ""
                    print(row)
                    self.df_comment.loc[len(self.df_comment)] = row
                except:
                    pass

            # if page_inner:
            #     self.comment_next(keywords, day=day, pn=pn)
            result=self.df_comment

        except Exception as e:
            print(e)
        finally:
            return result

    # 搜索转发
    def search_retweets(self, keyword, day=-365*50, pn=None):
        self.keyword = keyword
        result=None
        try:
            self.df_retweet = pd.DataFrame(columns=["mid", "user_id", "user_name", "retweet", "retweet_stamp", "retweet_date", "retweet_time", "like_count"])
            self.param['retweet']['id'] = keyword
            self.param['retweet']['page'] = 0
            # 翻页
            for index in range(1, pn+1):
                self.retweet_next(keyword, day=day, pn=pn)

            result=self.df_retweet

        except Exception as e:
            print(e)
        finally:
            return result

    # 转发翻页
    def retweet_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['retweet']['page']>=pn:
                    return result
                if self.param['retweet']['page']>100:
                    return result
            self.param['retweet']['page'] = self.param['retweet']['page'] + 1
            response = self.requests_get(self.urls['retweet'], data=self.param['retweet'], headers=self.headers['home'])
            # print(response.text)
            if response is None:
                return result
            web_content = json.loads(response.text)['data']['html']

            soup=BeautifulSoup(web_content, 'lxml')
            root_comments = soup.find_all('div', attrs={'class': re.compile("list_li S_line1 clearfix"),
                                                        'action-type': re.compile("feed_list_item")})
            for root in root_comments:
                try:
                    WB_text = root.find('div', class_='WB_text')
                    user_id = WB_text.a['usercard'].split('=')[-1].strip()
                    user_name = WB_text.a.text.strip()
                    content = WB_text.text.split('：')[-1].strip()
                    WB_from = root.find('div', class_='WB_from S_txt2')
                    user_stamp = WB_from.a['title']
                    user_date = WB_from.a['date']
                    user_time = WB_from.a.text.strip()
                    WB_handle = root.find('div', class_='WB_handle W_fr')
                    lis = WB_handle.find_all('li')
                    li1 = None
                    # li2=''
                    if lis:
                        li1 = lis[-1].text.replace('ñ', '').replace('赞', '0').strip()
                        # li2=lis[-2].text.strip()

                    row = [keyword, user_id, user_name, content, user_stamp, user_date, user_time, li1]
                    print(row)
                    # try:
                    #     news_date = datetime.datetime.strptime(news_stamp, "%Y年%m月%d日 %H:%M")
                    #     now = datetime.datetime.now()
                    #     delta = datetime.timedelta(days=day)
                    #     pre_date = now + delta
                    #     if news_date < pre_date:
                    #         continue
                    # except:
                    #     news_stamp = ""
                    # print(row)
                    self.df_retweet.loc[len(self.df_retweet)] = row
                except:
                    pass


            # if page_inner:
            #     self.retweet_next(keywords, day=day, pn=pn)
            result=self.df_retweet

        except Exception as e:
            print(e)
        finally:
            return result

    # 保存
    def excel_save(self):
        if self.df_retweet is not None:
            # self.df_detail.to_csv('detail_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_retweet.to_excel('retweet_{:s}.xlsx'.format(self.keyword))
        if self.df_comment is not None:
            # self.df_search.to_csv('search_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_comment.to_excel('comment_{:s}.xlsx'.format(self.keyword))
        if self.df_weibo is not None:
            # self.df_search.to_csv('search_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_weibo.to_excel('weibo_{:s}.xlsx'.format(self.keyword))

    # 搜索微博
    def search_weibo(self, keyword, day=-365*50, pn=None):
        self.keyword = keyword
        result=None
        try:
            self.df_weibo = pd.DataFrame(columns=['mid', 'user_id', 'user_name', 'idendity', 'member', 'weibo_stamp', 'weibo_date', 'weibo_time', 'source', 'original', 'content', 'retweet_count', 'comment_count', 'like_count', 'topics', 'at_users', 'retweet'])
            self.param['weibo']['id'] = '100606'+keyword
            self.param['weibo']['page'] = 0

            # for index in range(1, pn+1):
            self.weibo_next(keyword, day=day, pn=pn)

            result=self.df_weibo

        except Exception as e:
            print(e)
        finally:
            return result

    # 微博翻页
    def weibo_next(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['weibo']['page']>=pn:
                    return result
            # 下一页
            self.param['weibo']['page'] = self.param['weibo']['page'] + 1
            self.param['weibo']['pagebar'] = self.param['weibo']['pre_page'] =0
            response = self.requests_get(self.urls['weibo'], data=self.param['weibo'], headers=self.headers['home'])
            try:
                web_content = json.loads(response.text)['data']
            except:
                print('cookie失效')
                return
            if response is not None:
                web_content = json.loads(response.text)['data']
                self.weibo_parse(web_content)
            # 下拉翻页15
            self.param['weibo']['pre_page'] =self.param['weibo']['page']
            response = self.requests_get(self.urls['weibo'], data=self.param['weibo'], headers=self.headers['home'])
            if response is not None:
                web_content = json.loads(response.text)['data']
                self.weibo_parse(web_content)
            # 下拉翻页15
            self.param['weibo']['pagebar'] =1
            response = self.requests_get(self.urls['weibo'], data=self.param['weibo'], headers=self.headers['home'])
            if response is not None:
                web_content = json.loads(response.text)['data']
                self.weibo_parse(web_content)

            if r'下一页' in web_content:
                self.weibo_next(keyword, day=day, pn=pn)
            result=self.df_weibo

        except Exception as e:
            print(e)
        finally:
            return result

    # 解析微博
    def weibo_parse(self, web_content):
        soup = BeautifulSoup(web_content, 'lxml')
        list_item = soup.find_all('div', attrs={'action-data': re.compile("cur_visible=0"),
                                                    'action-type': re.compile("feed_list_item")})
        for item in list_item:
            try:
                mid = item['mid']
                ouid = item['tbinfo'].split('&')[0].split('=')[-1]

                WB_detail = item.find('div', class_='WB_detail')
                # print('id, 名字，认证，会员')
                WB_info = WB_detail.find('div', class_='WB_info').find_all('a')
                user_id = WB_info[0]['usercard'].split('&')[0].split('=')[-1].strip()
                user_name = WB_info[0].text.strip()
                renzheng = None
                huiyuan = None
                try:
                    renzheng = WB_info[1].i['title'].strip()
                    huiyuan = WB_info[2]['title'].strip()
                except:
                    pass
                # print('# 时间戳，来源')
                WB_from = WB_detail.find('div', class_='WB_from S_txt2').find_all('a')
                weibo_stamp = WB_from[0]['title']
                weibo_date = WB_from[0]['date'].strip()
                weibo_time = WB_from[0].text.strip()
                source = WB_from[1].text.strip() if len(WB_from) > 1 else None
                # 话题，@人员
                WB_text = WB_detail.find('div', class_='WB_text W_f14')
                content = WB_text.text.replace('\u200b\u200b\u200b\u200b', '').strip()
                topic = []
                atname = []
                exts = WB_text.find_all('a')
                for ext in exts:
                    try:
                        if ext['extra-data'] == 'type=topic':
                            topic.append(ext.text)
                        if ext['extra-data'] == 'type=atname':
                            atname.append(ext.text)
                    except:
                        pass
                if atname == []:
                    atname = None
                if topic == []:
                    topic = None

                WB_expand = WB_detail.find('div', class_='WB_feed_expand')
                origion = True if WB_expand else False
                retweet = None
                if origion:
                    retweet = self.parse_expand(WB_expand)
                # 转发评论点赞
                WB_handle = item.find('div', class_='WB_feed_handle')
                lis = WB_handle.find_all('li')
                zhuanfa = None
                pinglun = None
                dianzan = None
                try:
                    zhuanfa = lis[1].find_all('em')[1].text.strip()
                    pinglun = lis[2].find_all('em')[1].text.strip()
                    dianzan = lis[3].find_all('em')[1].text.strip()
                except:
                    pass

                row = [mid, user_id, user_name, renzheng, huiyuan, weibo_stamp, weibo_date, weibo_time, source, origion,
                       content, zhuanfa, pinglun, dianzan, topic, atname, retweet]
                # row=[mid, user_id, user_name, weibo_stamp, weibo_date, weibo_time, source, origion, content, zhuanfa, pinglun, dianzan, topic, atname, retweet]
                print(row)

                self.df_weibo.loc[len(self.df_weibo)] = row
            except Exception as e:
                print(e)
                pass


    # 解析转发
    def parse_expand(self, node):
        result={}
        try:
            # id, 名字，认证，会员
            WB_info = node.find('div', class_='WB_info').find_all('a')
            mid = WB_info[0]['suda-uatrack'].split(':')[-1].strip()
            user_id = WB_info[0]['usercard'].split('&')[0].split('=')[-1].strip()
            user_name = WB_info[0]['title'].strip()
            renzheng = None
            huiyuan = None
            try:
                renzheng = WB_info[1].i['title'].strip()
                huiyuan = WB_info[2]['title'].strip()
            except:
                pass
            # 时间戳，来源
            WB_from = node.find('div', class_='WB_from S_txt2').find_all('a')
            weibo_stamp = WB_from[0]['title']
            weibo_date = WB_from[0]['date'].strip()
            weibo_time = WB_from[0].text.strip()
            source = WB_from[1].text.strip() if len(WB_from) > 1 else None
            # 话题，@人员
            WB_text = node.find('div', class_='WB_text')
            content = WB_text.text.replace('\u200b\u200b\u200b\u200b','').strip()
            topic=[]
            atname =[]
            exts=WB_text.find_all('a')
            for ext in exts:
                try:
                    if ext['extra-data'] == 'type=topic':
                        topic.append(ext.text)
                    if ext['extra-data'] == 'type=atname':
                        atname.append(ext.text)
                except:
                    pass
            if atname==[]:
                atname=None
            if topic==[]:
                topic=None
            # 转发评论点赞
            WB_handle = node.find('div', class_='WB_handle W_fr')
            lis = WB_handle.find_all('li')
            zhuanfa = None
            pinglun = None
            dianzan = None
            try:
                zhuanfa = lis[0].find_all('em')[1].text.strip()
                pinglun = lis[1].find_all('em')[1].text.strip()
                dianzan = lis[2].find_all('em')[1].text.strip()
            except:
                pass

            row = [mid, user_id, user_name, renzheng, huiyuan, weibo_stamp, weibo_date, weibo_time, source, content,
                   zhuanfa, pinglun, dianzan, topic, atname]

            result = row
        finally:
            return result


    def get_json(self, params):
        """获取网页中json数据"""
        url = 'https://m.weibo.cn/api/container/getIndex?'
        # self.requests_get(url, data=params)
        r = requests.get(url,
                         params=params,
                         headers=self.headers['home'],
                         verify=False)
        return r.json()

    def get_weibo_json(self, page):
        """获取网页中微博json数据"""
        params = {
            "start_time": "2020-03-01",
            "end_time": "2020-09-30",
            'containerid': '107603' + self.keyword,
            'page': page
        }
        js = self.get_json(params)
        return js




    def get_user_info(self, keyword):
        """获取用户信息"""
        params = {'containerid': '100505' + keyword}
        js = self.get_json(params)
        if js['ok']:
            info = js['data']['userInfo']
            user_info = {}
            # user_info = OrderedDict()
            user_info['user_id'] = keyword
            user_info['user_name'] = info.get('screen_name', '')
            user_info['gender'] = info.get('gender', '')
            params = {
                'containerid':
                '230283' + keyword + '_-_INFO'
            }
            zh_list = [
                u'生日', u'所在地', u'小学', u'初中', u'高中', u'大学', u'公司', u'注册时间',
                u'阳光信用'
            ]
            en_list = [
                'birthday', 'location', 'education', 'education', 'education',
                'education', 'company', 'registration_time', 'sunshine'
            ]
            for i in en_list:
                user_info[i] = ''
            js = self.get_json(params)
            if js['ok']:
                cards = js['data']['cards']
                if isinstance(cards, list) and len(cards) > 1:
                    card_list = cards[0]['card_group'] + cards[1]['card_group']
                    for card in card_list:
                        if card.get('item_name') in zh_list:
                            user_info[en_list[zh_list.index(
                                card.get('item_name'))]] = card.get(
                                    'item_content', '')
            user_info['statuses_count'] = info.get('statuses_count', 0)
            user_info['followers_count'] = info.get('followers_count', 0)
            user_info['follow_count'] = info.get('follow_count', 0)
            user_info['description'] = info.get('description', '')
            user_info['profile_url'] = info.get('profile_url', '')
            user_info['profile_image_url'] = info.get('profile_image_url', '')
            user_info['avatar_hd'] = info.get('avatar_hd', '')
            user_info['urank'] = info.get('urank', 0)
            user_info['mbrank'] = info.get('mbrank', 0)
            user_info['verified'] = info.get('verified', False)
            user_info['verified_type'] = info.get('verified_type', -1)
            user_info['verified_reason'] = info.get('verified_reason', '')
            # user = self.standardize_info(user_info)

            # self.df_info=pd.DataFrame.from_dict(user_info,orient='index')
            # self.df_info.append(user_info, ignore_index=True)
            self.df_info.loc[len(self.df_info)]=user_info.values()

            return user_info

    def get_one_page(self, page):
        """获取一页的全部微博"""
        try:
            js = self.get_weibo_json(page)
            if js['ok']:
                weibos = js['data']['cards']
                for w in weibos:
                    # print(w)
                    if w['card_type'] == 9:
                        wb = self.get_one_weibo(w)
                        if wb:
                            # if wb['id'] in self.weibo_id_list:
                            #     continue
                            created_at = datetime.strptime(
                                wb['created_at'], '%Y-%m-%d')

                            #截止时间
                            end_date = datetime.strptime('2020-9-30', '%Y-%m-%d')
                            if created_at > end_date:
                                continue

                            since_date = datetime.strptime('2020-3-1', '%Y-%m-%d')
                            if created_at < since_date:
                                if self.is_pinned_weibo(w):
                                    continue
                                else:
                                    print(u'{}.已获取{}({})的第{}页微博{}'.format(
                                        '-' * 30, self.user['user_name'],
                                        self.user['user_id'], page, '-' * 30))
                                    return True
                            # if (not self.filter) or (
                            #         'retweet' not in wb.keys()):
                                # self.weibo.append(wb)
                                # self.weibo_id_list.append(wb['id'])
                                # self.got_count += 1
                            #     self.print_weibo(wb)
                            # else:
                            #     print(u'正在过滤转发微博')
            print(u'{}已获取{}({})的第{}页微博{}'.format(
                '-' * 30, self.user['user_name'], self.user['user_name'], page,
                '-' * 30))
        except Exception as e:
            print(e)


    def is_pinned_weibo(self, info):
        """判断微博是否为置顶微博"""
        weibo_info = info['mblog']
        title = weibo_info.get('title')
        if title and title.get('text') == u'置顶':
            return True
        else:
            return False



    def standardize_info(self, weibo):
        """标准化信息，去除乱码"""
        for k, v in weibo.items():
            if 'bool' not in str(type(v)) and 'int' not in str(
                    type(v)) and 'list' not in str(
                        type(v)) and 'long' not in str(type(v)):
                weibo[k] = v.replace(u'\u200b', '').encode(
                    sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding)
        return weibo


    def print_df(self, df):
        for index, row in df.iterrows():
            print(index)
            print(row)


    def start(self):
        self.update_info()

        df=self.search_comments('4555002956225080', pn=1)
        print(df)
        df=self.search_retweets('4555002956225080', pn=1)
        print(df)

        self.excel_save()

    def go(self):
        self.update_info()
        # df=self.search_weibo('1666052741', pn=3)
        # print(df)
        # df.to_excel('weibo.xlsx')
        #
        df=self.search_keywords('鲍毓明涉嫌性侵养女', pn=50)
        print(df)
        df.to_excel('鲍毓明涉嫌性侵养女_keyword.xlsx')

        # df = self.search_topics('#鲍某某涉嫌性侵案调查情况#', pn=50)
        # # df=self.search_topics('https://s.weibo.com/weibo?q=%23%E9%B2%8D%E6%9F%90%E6%9F%90%E6%B6%89%E5%AB%8C%E6%80%A7%E4%BE%B5%E6%A1%88%E8%B0%83%E6%9F%A5%E6%83%85%E5%86%B5%23', pn=50)
        # print(df)
        # df.to_excel('鲍毓明涉嫌性侵养女_topic.xlsx')




if __name__ == '__main__':

    ac=WeiboCrawl()
    # ac.start() 2518870750
    ac.go()







