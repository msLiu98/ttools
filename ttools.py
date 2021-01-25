import requests
import logging
import datetime
import math
from lxml import etree


class BaseTools(object):

    DEFAULT_DATE_FORMAT = "%Y-%m-%d"

    def date_list(self, start_date, end_date, **kwargs):
        """
        generate a list of dates
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


def geodis(coordinate_str, coor_mode=1):
    if coor_mode == 1:
        lng1, lat1, lng2, lat2 = coordinate_str.split(',')
    else:
        lat1, lng1, lat2, lng2 = coordinate_str.split(',')
    lng1, lat1, lng2, lat2 = map(
        math.radians,
        [float(lng1), float(lat1),
         float(lng2), float(lat2)])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    distance = 2 * math.asin(math.sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance / 1000, 3)
    return distance  # 单位：km


def replace_muni(scode):
    dict_munic = {
        1100: 1101,
        1200: 1201,
        3100: 3101,
        5000: 5001
    }
    return dict_munic.get(scode, scode)
