import tspider


class BaikeSpider(tspider.BaseSpider):

    name = 'baike'
    DEFAULT_PROXIES = '123'
    start_urls = ['https://www.baidu.com', 'https://baike.baidu.com/item/%E8%B4%BE%E8%B7%83%E4%BA%AD']

    # def start_requests(self):
    #     print(self.ROOT_URL)
    #     print(self.DEFAULT_PROXIES)


if __name__ == '__main__':
    from urllib.parse import unquote, quote
    url = 'https://baike.baidu.com/item/%E9%99%88%E5%BC%BA'
    word = '%E9%99%88%E5%BC%BA'
    print(unquote(word))
    word1 = '陈强'
    print(quote(word1))
