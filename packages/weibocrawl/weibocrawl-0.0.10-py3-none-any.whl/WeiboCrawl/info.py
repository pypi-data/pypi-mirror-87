#coding=utf-8

# import logging
# logging.basicConfig(filename='logging.log',
#                     format='%(asctime)s %(message)s',
#                     filemode="w", level=logging.DEBUG)

# 12.4更新：新增了话题和关键字的查询入口
# 12.5更新：修正新增了个人微博的查询search_weibo2


loginParam={

    "keyword": {
        "q": "鲍毓明涉嫌性侵养女",
        # "nodup": "1",
        # "Refer": "index",
        "page": 1,
    },

    "topic": {
        "q": "鲍毓明涉嫌性侵养女",
        "nodup": "1",
        "page": 1,
    },

    "retweet": {
        "ajwvr": "6",
        "id": "4554794956226910",
        "page": 1,
    },

    "comment": {
        "ajwvr": "6",
        "id": "4554794956226910",
        "page": 1,
        "filter": "hot",
        "sum_comment_number": "85",
        "filter_tips_before": "0",
        "from": "singleWeiBo",
    },

    "weibo": {
        "ajwvr": "6",
        "domain": "100606",
        "is_ori": "1",
        "is_forward": "1",
        "is_text": "1",
        "is_pic": "1",
        "is_video": "1",
        "is_music": "1",
        "is_article": "1",
        "key_word": "",
        "start_time": "2020-03-01",
        "end_time": "2020-09-30",
        "is_search": "1",
        "is_searchadv": "1",
        "pagebar": 0,
        "pl_name": "Pl_Official_MyProfileFeed__23",
        "id": "1006061742666164",
        "script_uri": "/lancome",
        "feed_type": "0",
        "page": 1,
        "pre_page": 0,
        "domain_op": "100606",
        # "__rnd": "1606325093740"
    },

    "weibo2": {
        "is_search": "1",
        "visible": "0",
        "is_ori": "1",
        "is_pic": "1",
        "is_video": "1",
        "is_music": "1",
        "is_article": "1",
        "is_forward": "1",
        "is_text": "1",
        "start_time": "2020-03-01",
        "end_time": "2020-09-30",
        "is_tag": "0",
        "profile_ftype": "1",
        "page": 1,
        "pagebar": 0,
        "pre_page": 0,
    }

}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxies': {
        # "http": 'http://127.0.0.1:80',
        "https": 'https://127.0.0.1:1080'
    },
    "retweet":"https://weibo.com/aj/v6/mblog/info/big?",
    "comment":"https://weibo.com/aj/v6/comment/big?",
    "weibo":"https://weibo.com/p/aj/v6/mblog/mbloglist?",
    "weibo2":"https://weibo.com/u/{:s}?",
    "keyword":"https://s.weibo.com/weibo?",
    "topic":"https://s.weibo.com/weibo?",
    "base":"https://weibo.com/u/{:s}?",


}
loginHeaders = {

    "home": {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "SINAGLOBAL=5579701838206.736.1605880029171; wvr=6; SSOLoginState=1607050973; _s_tentry=login.sina.com.cn; Apache=5341830820140.594.1607050977038; UOR=login.sina.com.cn,weibo.com,login.sina.com.cn; ULV=1607050977044:12:3:4:5341830820140.594.1607050977038:1606904618796; wb_view_log_3479726797=1536*8641.25; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWgxyR8DlA5uOfXLUFsnVlP5JpX5KMhUgL.FoeXS0.NeoqN1KM2dJLoI7_DMcHfSoqcP0zEe5tt; ALF=1638680951; SCF=Alx6A-qiJFwbh6ziknk_s1AyMls2FBOF9t8ivMLmXxCSn-LmnRV6lU7Nwr7PhyJIbBYt1fM8ag6qAS92fU85PI8.; SUB=_2A25yz2WpDeRhGeVK7FsW8ijLwjuIHXVRvdBhrDV8PUNbmtAKLRelkW9NTCmebj-mB-kEeUSeogSTiG8fjbsiihfS; webim_unReadCount=%7B%22time%22%3A1607144972341%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A42%2C%22msgbox%22%3A0%7D",
        # "referer": "https://weibo.com/lancome?is_hot=1&sudaref=passport.weibo.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41",
        "x-requested-with": "XMLHttpRequest"
    },

    "weibo": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "SINAGLOBAL=5579701838206.736.1605880029171; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWgxyR8DlA5uOfXLUFsnVlP5JpX5KMhUgL.FoeXS0.NeoqN1KM2dJLoI7_DMcHfSoqcP0zEe5tt; ALF=1638586972; SSOLoginState=1607050973; SCF=Alx6A-qiJFwbh6ziknk_s1AyMls2FBOF9t8ivMLmXxCSqYAVUJ8TTXD9J_83neTt1tilyMIOturzLjenq-yltJA.; SUB=_2A25yzdaODeRhGeVK7FsW8ijLwjuIHXVRu09GrDV8PUNbmtANLUf7kW9NTCmebk2pZcIhTzIUcg1_6YKDpMMd38Nc; _s_tentry=login.sina.com.cn; UOR=login.sina.com.cn,weibo.com,login.sina.com.cn; Apache=5341830820140.594.1607050977038; ULV=1607050977044:12:3:4:5341830820140.594.1607050977038:1606904618796; webim_unReadCount=%7B%22time%22%3A1607053691120%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A42%2C%22msgbox%22%3A0%7D",
        "Host": "s.weibo.com",
        "Referer": "https",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52"
    },



}

loginMsg='''

https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C+%E7%94%B5%E5%AD%90%E9%93%B6%E8%A1%8C&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn=10


'''

loginCookie='wxuin=1610134497; devicetype=android-24; version=2607023a; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=n7zaWPtBa5p3vItJykj3ZkhXHZ3HchLLwnoEsl+lH2ICQgOCN0EXBSUl85YaESOe; wap_sid2=COHn4v8FEooBeV9ITm1XYmY2bE9rWkpTZDZxbEljVTRpWWdQUkVNbFNxNk1SNURWQWlSVWpzbF9PbnVWb3piN1hERk9rVVBtQ0VHTEdxVVdObjNWZEptSkxVRk5SbDNubTBFdXRYRmIyYVcxazViTUgxOFFJNEkwTkNXVzl5SXhRblRiV3RGb3FzeXR4d1NBQUF+MPvxpf0FOA1AAQ=='

