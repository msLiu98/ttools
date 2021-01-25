import requests
import logging


class BaseSpider(object):

    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    DEFAULT_PROXIES = None
    DEFAULT_COOKIES = None

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

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")

        for url in self.start_urls:
            self.parse(self.get(url))

    def parse(self, response, **kwargs):
        raise NotImplementedError(f'{self.__class__.__name__}.parse callback is not defined')