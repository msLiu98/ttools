import requests
import logging
import re
from lxml import etree
import pandas as pd
import os
import sys
from .utils import *


class BaseSpider(object):

    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    DEFAULT_PROXIES = None
    DEFAULT_COOKIES = {}

    start_urls = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError(f"{type(self).__name__} must have a name")
        self.__dict__.update(kwargs)

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)

    def get(self, url, params=None, meta=None):
        if meta:
            cookies = meta.get('cookies', self.DEFAULT_COOKIES)
            proxies = meta.get('proxies', self.DEFAULT_PROXIES)
            headers = meta.get('headers', self.DEFAULT_HEADERS)
            if isinstance(cookies, str):
                cookies = trans_cookie(cookies)
            return requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
        else:
            return requests.get(url, headers=self.DEFAULT_HEADERS)

    def post(self, url, data, meta=None):
        if not data:
            raise ValueError("Post request must have data")
        if meta:
            cookies = meta.get('cookies', self.DEFAULT_COOKIES)
            headers = meta.get('headers', self.DEFAULT_HEADERS)
            proxies = meta.get('proxies', self.DEFAULT_PROXIES)
            return requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies)
        else:
            return requests.post(url, data=data, headers=self.DEFAULT_HEADERS)

    def set_proxies(self, proxies):
        self.DEFAULT_PROXIES = proxies

    def start_requests(self, urls):
        for url in urls:
            self.get(url)


class BaseLoader(object):

    DEFAULT_DATA_TYPE = 'text'
    output = {}
    html = ''

    def __init__(self, response, **kwargs):
        self.response = response
        self.__dict__.update(kwargs)

    def add_xpaths(self, xpaths: dict, axis=0):
        if xpaths:
            self._set_html()
            if axis == 0:
                for key, xpath in xpaths.items():
                    self.output[key] = self.html.xpath(xpath)
            else:
                xp_parent = xpaths.get('parent')
                eles_parent = self.html.xpath(xp_parent)
                list_dict = []
                for ele_child in eles_parent:
                    dict_data = {}
                    for key, xpath in xpaths.get('children').items():
                        dict_data[key] = ele_child.xpath(xpath)
                    list_dict.append(dict_data)
                self._set_output(list_dict)
        else:
            self._set_json()

    def _set_output(self, output):
        self.output = output

    def _set_html(self):
        self.html = etree.HTML(self.response.content.decode())

    def _set_json(self):
        self.output.update(self.response.json())

    def check_lens(self, dict_data):
        format_output = {}
        list_lens = [len(v) for v in self.output.values()]
        max_len = max(list_lens)
        min_len = min(list_lens)
        if max_len == min_len:
            return pd.DataFrame(self.output)
        else:
            for k, v in self.output.items():
                if len(v) < max_len:
                    v.extend([''] * (max_len - len(v)))
                format_output[k] = v
            return pd.DataFrame(format_output)

    def load_items(self):
        return pd.DataFrame(self.output)


class BasePipeline(object):

    def __init__(self, file_name):
        if not file_name:
            file_name = 'data.csv'
        self.file_name = file_name
        self.dir_data = 'data'

    def to_csv(self, data, over_write=None):
        assert isinstance(data, pd.DataFrame)
        if not os.path.exists(self.dir_data):
            os.mkdir(self.dir_data)

        file_path = f'{self.dir_data}/{self.file_name}'
        if over_write:
            data.to_csv(file_path, index=False)
        else:
            if not os.path.exists(file_path):
                data.to_csv(file_path, mode='a+', index=False)
            else:
                data.to_csv(file_path, mode='a+', index=False, header=False)


class BaseScheduler(object):

    def __init__(self, name, configs):
        self.name = name
        self.meta = configs

    def check_configs(self):

        return

    def run(self):
        bspider = BaseSpider(self.name)
        url = self.meta.get('url', None)
        req = bspider.get(url=url, meta=self.meta)
        self.set_response(req)
        print('Successfully crawled')

        loader = BaseLoader(req)
        xpaths = self.meta.get('xpaths', None)
        axis = self.meta.get('xpaths_axis', 0)
        loader.add_xpaths(xpaths, axis)
        data = loader.load_items()

        file_name = self.meta.get('file_name', None)
        over_write = self.meta.get('over_write', None)
        pipe = BasePipeline(file_name)
        pipe.to_csv(data, over_write=over_write)
        bspider.log("Crawling complete!")

    def set_response(self, response):
        self.response = response

    def get_html(self):
        return etree.HTML(self.response.text)


if __name__ == '__main__':
    print(os.getcwd())
