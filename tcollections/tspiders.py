# -*-coding:utf-8-sig -*-

import requests
from lxml import etree
import re
import pymysql
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


class Tspiders(object):

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            # "Host": "index.baidu.com",
            # "Referer": "https://index.baidu.com/v2/main/index.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        }
        # self.html = ''

    def get(self, url, params=None, cookie=None):
        cookies = cookie
        if cookie:
            cookies = self.trans_cookies(cookie)
        r = requests.get(url, params=params, cookies=cookies)
        self.preprocess_req(r)

    def post(self, url, data=None, cookie=None):
        cookies = cookie
        if cookie:
            cookies = self.trans_cookies(cookie)
        r = requests.post(url, data=data, cookies=cookies)
        self.preprocess_req(r)

    def preprocess_req(self, req):
        req.raise_for_status()
        try:
            self.jsobj = req.json()
            return req.json()
        except Exception as e:
            print(e)
            text = req.content.decode()
            self.text = text
            return text

    def extract_by_xpath(self, xpaths: dict, maps=None):
        html = self.text_to_html(self.text)
        if len(html) == 0:
            raise ValueError('No html, check it!')
        output = {}
        for item in xpaths.keys():
            xpath = xpaths[item]
            try:
                html_data = html.xpath(xpath)
                if maps:
                    for map_func in maps:
                        html_data = map_func(html_data)
            except Exception as e:
                raise Exception(f"Something wrong with the xpath: {xpath}")
            output[item] = html_data
        return output

    def extract_by_json(self):
        js_obj = json.loads(self.text)
        return js_obj

    @staticmethod
    def trans_cookies(cookie):
        cookies = {}
        for item in cookie.split(';'):
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            cookies[key] = value
        return cookies

    @staticmethod
    def text_to_html(text):
        pat_sub = re.compile('\xa0|&nbsp|\n|\r')
        text_parsed = re.sub(pat_sub, '', text)
        html = etree.HTML(text_parsed, parser=etree.HTMLParser())
        return html


class Tprocessors(object):

    def __init__(self):
        print()

    @staticmethod
    def join(data: list, sep='$'):
        return sep.join(data)

    @staticmethod
    def no_null(data: list):
        data_no_null = list()
        for i in data:
            if i.strip():
                data_no_null.append(i)
        return data_no_null

    @staticmethod
    def text_to_html(text):
        pat_sub = re.compile('\xa0|&nbsp|\n|\r')
        text_parsed = re.sub(pat_sub, '', text)
        html = etree.HTML(text_parsed, parser=etree.HTMLParser())
        return html

    @staticmethod
    def extract_by_xpath(html, xpaths: dict, maps=None):
        if len(html) == 0:
            raise ValueError('No html, check it!')
        output = {}
        for item, xpath in xpaths.items():
            try:
                html_data = html.xpath(xpath)
                if maps:
                    for map_func in maps:
                        html_data = map_func(html_data)
            except Exception as e:
                raise Exception(f"Something wrong with the xpath: {xpath}")
            output[item] = html_data
        return output

    @staticmethod
    def extract_by_xpath_allinone(html, xpaths: dict, maps=None):
        if len(html) == 0:
            raise ValueError('No html, check it!')
        output = {}
        for item, xpath in xpaths.items():
            try:
                xp_cont, xp_elem = xpath[::-1].split('/', 1)
                xp_cont = '/' + xp_cont[::-1] if xp_elem[::-1].endswith('/') else xp_cont[::-1]
                xp_elem = xp_elem[::-1][:-1] if xp_elem[::-1].endswith('/') else xp_elem[::-1]
                # print(xp_elem)
                # print(xp_cont)
                html_data = html.xpath(xp_elem)
                lst_txtdata = []
                nums = len(html_data)
                for i in range(1, nums + 1):
                    text_data = '|'.join(html.xpath(f'{xp_elem}[{i}]/{xp_cont}'))
                    lst_txtdata.append(text_data)
                if maps:
                    for map_func in maps:
                        html_data = map_func(html_data)
            except Exception as e:
                raise Exception(f"Something wrong with the xpath: {xpath}")
            output[item] = lst_txtdata
        return output

    @staticmethod
    def extract_by_xpath_inbox(html, xpaths: dict, maps=None):
        xpaths = xpaths.copy()
        if len(html) == 0:
            raise ValueError('No html, check it!')
        output = {}
        xp_box = xpaths['xpath_box']
        xpaths.pop('xpath_box')
        html_boxes = html.xpath(xp_box)
        for item, xpath in xpaths.items():
            try:
                xp_cont, xp_elem = xpath[::-1].split('/', 1)
                xp_cont = '/' + xp_cont[::-1] if xp_elem[::-1].endswith('/') else xp_cont[::-1]
                xp_elem = xp_elem[::-1][:-1] if xp_elem[::-1].endswith('/') else xp_elem[::-1]
                lst_txtdata = []
                nums = len(html_boxes)
                for i in range(1, nums + 1):
                    text_data = '|'.join(html.xpath(f'{xp_box}[{i}]{xp_elem}/{xp_cont}'))
                    lst_txtdata.append(text_data)
                # if maps:
                #     for map_func in maps:
                #         html_data = map_func(html_data)
            except Exception as e:
                raise Exception(f"Something wrong with the xpath: {xpath}")
            output[item] = lst_txtdata
        return output

    @staticmethod
    def extract_by_re(text, res: dict, maps=None):
        if len(text) == 0:
            raise ValueError('No html, check it!')
        output = {}
        for item, reg in res.items():
            try:
                text_data = re.findall(reg, text)
                if maps:
                    for map_func in maps:
                        text_data = map_func(text_data)
            except Exception as e:
                raise Exception(f"Something wrong with the xpath: {reg}")
            output[item] = text_data
        return output


def get_mcgov():
    ts = Tspiders()
    tp = Tprocessors()
    url_mcgov = 'http://www.mca.gov.cn//article/sj/xzqh/2020/2020/2020092500801.html'
    ts.get(url_mcgov)
    xpaths = {
        'title': '//td[@class="xl7424734"]//text()',
        'column1': '//td[@class="xl6624734"]/text()',
        'scode': '//td[@class="xl7024734"]//text()',
        'adcode': '//td[@class="xl7124734"]//text()',
    }
    data = ts.extract_by_xpath(xpaths, [tp.no_null])
    print(data)


if __name__ == '__main__':
    get_mcgov()
    # TODO: 完善个人 general 爬虫
    #
