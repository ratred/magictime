# -*- coding: utf-8 -*-

import locale
import time
import re

from dateutil.parser import parse
from datetime import datetime, time as ltime
from time import mktime as mktime, time as ttime
           
'''
    Магический ооочень простой объект времени
'''

class magictime:
    tformat  = '%d %b %Y %H:%M:%S'
    mysqlformat = '%Y%m%d%H%M%S'

    def __cmp__(self, other):
        if not isinstance(other, magictime):
            other = magictime(other)
        if self.unixtime > other.unixtime:
            return 1
        elif self.unixtime < other.unixtime:
            return -1
        else:
            return 0

    def __init__(self, time='0', **kwargs):
        self.original   = 0
        self.asctime    = ''
        self.unixtime   = 0
        self.msectime   = 0
        self.mcsectime  = 0
        self.t          = time
        self.mysql      = ''

        rexp = re.match('^([12][90][012]\d)([01][0-9])([0123][0-9])(\d\d)(\d\d)(\d\d)', str(time))

        if time is None:                                                              # Nonetype. Считаем, что время равно нулю
            time = 0
            self.asctime  = datetime.fromtimestamp(time).strftime(self.tformat)
            self.mysql    = datetime.fromtimestamp(time).strftime(self.mysqlformat)
            self.unixtime = 0
            self.msectime = 0
        elif isinstance(time, datetime):                                              # datetime тип (нафик он нам тут?)
            self.asctime  = time.strftime(self.tformat)
            self.mysql    = time.strftime(self.mysqlformat)
            self.unixtime = int(mktime(time.timetuple()))
            self.msectime = self.unixtime * 1000000
        elif re.match('^\d+$', str(time)): 
            time = int(time)
            if time == 0:                                                           # Текущее время
                time = int(ttime())
                self.original = str(time)
                self.asctime  = datetime.fromtimestamp(time).strftime(self.tformat)
                self.mysql    = datetime.fromtimestamp(time).strftime(self.mysqlformat)
                self.unixtime = time
                self.msectime = time * 1000000
            elif rexp and int(rexp.group(1)) > 1970 and int(rexp.group(1)) < 2025:  # Это mysql timestamp
                time = str(time)
                parsed = parse(time,  fuzzy_with_tokens=True)
                restime = int(mktime(parsed[0].timetuple()))
                self.original = time
                self.unixtime = restime
                self.msectime = restime * 1000000
                self.mysql    = time
                self.asctime  = parsed[0].strftime(self.tformat).encode('utf-8')
            elif time > 0 and time < 4294967296:                                    # Это наверняка unixtime
                self.original = time
                self.asctime  = datetime.fromtimestamp(time).strftime(self.tformat)
                self.mysql    = datetime.fromtimestamp(time).strftime(self.mysqlformat)
                self.unixtime = time
                self.msectime = time * 1000000
            elif time > 9999999999 and time < 99999999999999999:                    # Скорее всего это время в микросекундах
                self.original = time
                self.unixtime = int(time/1000000)
                self.asctime  = datetime.fromtimestamp(self.unixtime).strftime(self.tformat) 
                self.msectime = time
                self.mysql    = time
            else: 
                return None
        else:                                                                           # Это, предположительно, 
            time = str(time.decode('utf-8'))                                            # время в текстовом формате
            parsed = parse(time,  fuzzy_with_tokens=True)
            restime = int(mktime(parsed[0].timetuple()))
            self.original = time.encode('utf-8')
            self.unixtime = restime
            self.msectime = restime * 1000000
            self.mysql    = parsed[0].strftime(self.mysqlformat).encode('utf-8')
            self.asctime  = parsed[0].strftime(self.tformat).encode('utf-8')
        return None

