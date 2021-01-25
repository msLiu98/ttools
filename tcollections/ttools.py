import requests
import logging
import datetime
from lxml import etree


class BaseSpider(object):

    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    DEFAULT_PROXIES = None
    DEFAULT_COOKIES = None

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

    def get(self, url, meta=None, **kwargs):
        if meta:
            req_meta = meta.copy()
            req_meta.update(kwargs)
            params = req_meta.get('params', None)
            cookies = req_meta.get('cookies', self.DEFAULT_COOKIES)
            proxies = req_meta.get('proxies', self.DEFAULT_PROXIES)
            headers = req_meta.get('headers', self.DEFAULT_HEADERS)
            return requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
        else:
            return requests.get(url, headers=self.DEFAULT_HEADERS)

    def post(self, url, meta):
        data = meta.get('data', None)
        if not data:
            raise ValueError("Post request must have data")
        cookies = meta.get('cookies', self.DEFAULT_COOKIES)
        headers = meta.get('headers', self.DEFAULT_HEADERS)
        proxies = meta.get('proxies', self.DEFAULT_PROXIES)
        return requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies)

    def set_proxies(self, proxies):
        self.DEFAULT_PROXIES = proxies


class BaseLoader(object):

    DEFAULT_DATA_TYPE = 'text'
    output = {}

    def __init__(self, response, **kwargs):
        self.response = response
        self.__dict__.update(kwargs)

    @property
    def html(self):
        return etree.HTML(self.response.content.decode())

    def add_xpaths(self, xpaths: dict):
        for key, xpath in xpaths.items():
            self.output[key] = self.html.xpath(xpath)


class BasePipeline(object):

    def __init__(self):
        pass


class BaseTools(object):

    DEFAULT_DATE_FORMAT = "%Y-%m-%d"

    def date_range(self, start_date, end_date, **kwargs):
        """

        @param start_date:
        @param end_date:
        @param kwargs:
        @return: includes start_date but not end_date
        """
        date_fmt = kwargs.get('date_fmt', self.DEFAULT_DATE_FORMAT)
        start_date = datetime.datetime.strptime(start_date, date_fmt)
        end_date = datetime.datetime.strptime(end_date, date_fmt)
        days = (end_date - start_date).days
        return [(start_date+datetime.timedelta(days=d)).strftime(date_fmt) for d in range(days)]

    def trans_cookie(self, cookie_str):
        cookies = {}
        items = cookie_str.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            cookies[key] = value
        return cookies
