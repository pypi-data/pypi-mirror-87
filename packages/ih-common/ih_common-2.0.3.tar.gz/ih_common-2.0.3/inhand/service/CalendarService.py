import http.client
import json
import time
import ssl
import requests
from datetime import datetime
from urllib import parse
import logging,traceback

class CalendarService:
    def __init__(self,settings):
        import sys
        sys.path.append('../../')
        from utilities.URLUtility import GenericURL
        self.settings = settings
        ssl._create_default_https_context = ssl._create_unverified_context


    # 月份
    def query(self,year,month):
        raise  NameError('This is a parent class, there is nothing to do!')


    @staticmethod
    def createCalendarService(settings):
        if settings.app.calendar_provider == 'baidu':
            return BaiduCalendarService(settings)
        else:
            return None



class BaiduCalendarService(CalendarService):
    def __init__(self,settings):
        CalendarService.__init__(self,settings)
        self.calendar_provider = self.settings.app.calendar_provider
        self.calendar_url = self.settings.app.calendar_url
    # 输入参数：月份
    def query(self,year,month):
        url = self.calendar_url
        bits = list(parse.urlparse(url))
        qs = parse.parse_qs(bits[4])
        qs['query'] = '{}年{}月'.format(year,month)
        bits[4] = parse.urlencode(qs, True)
        url = parse.urlunparse(bits)
        lst = []
        lst1 = []
        lst2 = []
        lst3 = []
        try:
            r = requests.get(url)
            f = r.json()
            holiday = f['data'][0]['holiday']

            for i in range(len(holiday)):
                if len(holiday[i]['list']) == 1:
                    lst.append(holiday[i]['list'][0])
                else:
                    for j in range(len(holiday[i]['list'])):
                        lst.append(holiday[i]['list'][j])
            for i in range(len(lst)):
                for key in lst[i].keys():
                    t = lst[i][key]
                    lst1.append(t)

            for i in range(len(lst1)):
                if (i % 2) == 0:
                    lst2.append(lst1[i])
                else:
                    lst3.append(lst1[i])

            for i in range(len(lst2)):
                lst2[i] = datetime.strptime(lst2[i], '%Y-%m-%d').strftime('%Y-%m-%d')

            # del (dict)
            dit = dict(map(lambda x, y: [x, int(y)], lst2, lst3))
            return dit
        except Exception as e:
            logging.warning("While call %s, There is an exception: %s" % (self.url.host,e))
            return None

if __name__ == '__main__':
    import sys

    sys.path.append('../../')
    from Settings import Settings
    settings=Settings.readLocalSettings(path="../../../../test.json")

    calcendar = CalendarService.createCalendarService(settings)
    ret = calcendar.query('2020','09')
    print(ret)
    ret = calcendar.query(2019,9)
    print(ret)

