from tspider.tspider import *
import os


def test1():
    district = 'wh'
    url = f'https://{district}.lianjia.com/ershoufang/'
    get_info = {
        'url': url,
        'headers': None,
        'cookies': None,
        'proxies': None,
        'xpaths': {
            'title': '//li[@class="clear LOGVIEWDATA LOGCLICKDATA"]/div[@class="info clear"]/div[@class="title"]/a/text()'
        },
        'file_name': 'lianjia_wh.csv',
        'over_write': True,
    }
    bs = BaseScheduler('lianjia', get_info)
    bs.run()


def test2():
    url = 'http://www.mca.gov.cn/article/sj/xzqh/1980/2019/202002281436.html'
    get_info = {
        'url': url,
        'headers': None,
        'cookies': None,
        'proxies': None,
        'xpaths': {
            'parent': '//tr[@height="19"]',
            'children': {  # No forward slash before child xpath
                'adcode': 'td[2]/text()',
                'name': 'td[3]/text()',
            }
        },
        'xpaths_axis': 1,
        'file_name': 'mcagov.csv',
        'over_write': False,
    }
    bs = BaseScheduler('xzqh', get_info)
    bs.run()


def test3():
    api_root = 'https://www.av01.tv'
    url = 'https://www.av01.tv/search/videos?search_query=%E6%A1%83%E4%B9%83%E6%9C%A8'  # 一级页面，检索界面
    # 二级页面 视频页面
    url2 = 'https://www.av01.tv/video/32046/ipz-855-%E3%82%B9%E3%82%AD%E3%83%A3%E3%83%B3%E3%83%80%E3%83%AB-%E7%86%B1%E6%84%9B%E7%B7%A8-%E7%9C%9F%E5%89%A3%E4%BA%A4%E9%9A%9B%E3%81%A7%E3%81%8A%E6%8C%81%E3%81%A1%E5%B8%B0%E3%82%8A%E3%81%95%E3%82%8C%E3%81%9F%E6%A1%83%E4%B9%83%E6%9C%A8%E3%81%8B%E3%81%AA-%E7%9B%97%E6%92%AE%E6%98%A0%E5%83%8F-%E3%81%9D%E3%81%AE%E3%81%BE%E3%81%BEav%E7%99%BA%E5%A3%B2-180%E5%88%86special'
    get_info = {
        'url': url,
        'headers': None,
        'cookies': None,
        'proxies': {
            'http': 'http://127.0.0.1:10809',
            'https': 'http://127.0.0.1:10809'
        },
        'xpaths': {
            'parent': '//div[@class="col-md-9 col-sm-8"]/div[2]/div',
            'children': {  # No forward slash before child xpath
                'href': 'div[@class="well well-sm "]/a/@href',
                'title': 'div[@class="well well-sm "]/a/span/text()',
                'videocode': 'div[@class="well well-sm "]//div[@class="fa pull-left"]/text()',
                'actress': 'div[@class="well well-sm "]//div[@class="fa pull-right"]/a/text()',
                'abstract': 'div[@class="well well-sm "]//div[@class="video-added title-truncate"]/text()'
            }
        },
        'xpaths_axis': 1,
        'file_name': 'ainfo.csv',
        'over_write': True,
    }
    get_info2 = {
        'url': url2,
        'headers': None,
        'cookies': None,
        'proxies': {
            'http': 'http://127.0.0.1:10809',
            'https': 'http://127.0.0.1:10809'
        },
        'xpaths': {
            'parent': '//div[@class="col-sm-6 col-md-3 col-lg-3"]/div',
            'children': {  # No forward slash before child xpath
                'href': 'a/@href',
                'title': 'a/span[@class="video-title title-truncate m-t-5"]/text()',
                'abstract': 'div[@class="video-added title-truncate"]/text()',
                'videocode': 'div[@class="video-views"]/div[@class="fa pull-left"]/text()',
                'actress': 'div[@class="video-views"]/div[@class="fa pull-right"]/a/text()',
                'thumb_link': 'a//div[@class="av01-cover-ineer"]/img/@data-src',
                'duration': 'a/div/div[3]/text()'
            }
        },
        'xpaths_axis': 1,
        'file_name': 'ainfo.csv',
        'over_write': True,
    }
    bs = BaseScheduler('ainfo2', get_info2)
    bs.run()

    return


if __name__ == '__main__':
    print(os.getcwd())
    test3()
