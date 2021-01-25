import sys
import tspiders
import ttools
import requests
import asyncio
import aiohttp

sys.path.append(r'E:\Projects\Scrapy\tcollections')


def test1():
    url = 'https://baike.baidu.com/item/%E6%9D%8E%E5%88%9A/5335'
    ts = tspiders.Tspiders()
    bs = ttools.BaseSpider('bs1')
    meta1 = {
        'params': {
            'test': 'test'
        }
    }
    req = bs.get(url=url)
    bl = ttools.BaseLoader(req, data_type='text')
    xpaths = {
        'title': '//ul[@class="polysemantList-wrapper cmn-clearfix"]/li/a/@title'
    }
    bl.add_xpaths(xpaths)
    print(bl.output)


def test2():
    url = 'https://www.baidu.com'
    proxies = None
    params = None
    req = requests.get(url, proxies=proxies, params=params)
    print(req.status_code)
    print(req.content.decode())


def test3():
    import datetime

    start = datetime.datetime.strptime('2010-11-21', "%Y-%m-%d")
    end = datetime.datetime.strptime('2010-12-21', "%Y-%m-%d")
    print(end-start)
    print(type(end-start))
    print((end-start).days)
    tt = ttools.BaseTools()
    print(tt.date_range('2010-11-21', '2010-12-21'))


class Spider(ttools.BaseSpider):
    name = '1'

    def get(self):
        print(1)


def test4():
    s = Spider()
    s.get()


if __name__ == '__main__':
    test4()
