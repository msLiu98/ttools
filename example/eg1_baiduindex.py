from tspider.tspider import *
from urllib.parse import quote


def baidu_index():

    ts = BaseSpider('baiduindex')
    api_search_index = r'http://index.baidu.com/api/SearchApi/index?'
    # api_feed_index = r'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?'
    # api_news_index = r'https://index.baidu.com/api/NewsApi/getNewsIndex?'

    cookies = 'BAIDUID=3E7A350914CE7B7B8CBA5FAFE34E14A0:FG=1; BIDUPSID=3E7A350914CE7B7B8CBA5FAFE34E14A0; PSTM=1595043302; BDUSS=NqV1B2aXhjb3UwcGRqeWJueVdSaDZTdUdRWmcxaXI3V0ptaUh1Uzd-TEhFSVZmRVFBQUFBJCQAAAAAAAAAAAEAAACiFZmRbHQxMjM0YXNkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMeDXV~Hg11fZH; MCITY=-%3A; bdindexid=1fehmpkmn93mbr7ofi4gr11pg0; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1600010949,1601963822,1602479774,1602511696; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1602511735; __yjsv5_shitong=1.0_7_d7a218f80eecbd721fdef5756093aead69f7_300_1602511735894_58.247.22.183_0c46a2f7; RT="z=1&dm=baidu.com&si=r2la5jozbi&ss=kg6m35rr&sl=d&tt=9f9&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=wcr"'
    cookies = 'H_WISE_SIDS=;STOKEN=89b5708cfcbc4f5d8b3a8e53b1217171fac51fc74340cfd52a902d502a548815;BDUSS=1dVZW5qb1o1LVk0eFoyUnlnaWthYWEwa0hBRGNOSnBQVk1JaWJSSjI4MGhDeHBmRVFBQUFBJCQAAAAAAAAAAAEAAADnnBVo0KHHyc620uS-44nVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACF-8l4hfvJeR;PTOKEN=0fb896de0f2440e993d1e51cd6d40458;BAIDUID=69FE44C662BD1B2AB9ECC1EFF3EA435B:FG=1'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "index.baidu.com",
        "If-Modified-Since": "Sat, 09 May 2020 06:42:21 GMT",
        "Referer": "https://index.baidu.com/v2/main/index.html",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    words = '龚正,赵瑞东,邓群策,李锐,田学仁'.split(',')
    q1, q2, q3, q4, q5 = (quote(w) for w in words)
    area = 0
    url = f'{api_search_index}' \
          f'area={area}' \
          f'&word=[[%7B%22name%22:%22{q1}%22,%22wordType%22:1%7D],[%7B%22name%22:%22{q2}%22,%22wordType%22:1%7D],[%7B%22name%22:%22{q3}%22,%22wordType%22:1%7D],[%7B%22name%22:%22{q4}%22,%22wordType%22:1%7D],[%7B%22name%22:%22{q5}%22,%22wordType%22:1%7D]]'

    meta = {
        'headers': headers,
        'cookies': cookies
    }
    jsobj = ts.get(url, meta=meta).json()
    print(jsobj)
    return


if __name__ == '__main__':
    baidu_index()
