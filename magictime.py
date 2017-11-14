# -*- coding: utf-8 -*-

import locale
import time
import re

from dateutil.parser import parse
from datetime import datetime, time
from time import mktime as mktime
           
'''
    Very simple time object
'''

class magictime:
    tformat  = '%d %b %Y %H:%M:%S'
    mysqlformat = '%Y%m%d%H%M%S'

    def __cmp__(self, other):
        if self.unixtime > other.unixtime:
            return 1
        elif self.unixtime < other.unixtime:
            return -1
        else:
            return 0

    def __init__(self,time='0', **kwargs):
        self.original   = 0
        self.asctime    = ''
        self.unixtime   = 0
        self.msectime   = 0
        self.mcsectime  = 0
        self.t          = time
        self.mysql      = ''

        rexp = re.match('^([12][90][012]\d)([01][0-9])([0123][0-9])(\d\d)(\d\d)(\d\d)', time)

        if re.match('^\d+$', str(time)): 
            time = int(time)
            if time == 0:                                                           # Current time
                time = int(self.t.time())
                self.original = str(time)
                self.asctime  = datetime.fromtimestamp(time).strftime(self.tformat)
                self.mysql    = datetime.fromtimestamp(time).strftime(self.mysql)
                self.unixtime = time
                self.msectime = time * 1000000
            elif rexp and int(rexp.group(1)) > 1970 and int(rexp.group(1)) < 2025:  # Possible it is mysql timestamp
                time = str(time)
                parsed = parse(time,  fuzzy_with_tokens=True)
                restime = int(mktime(parsed[0].timetuple()))
                self.original = time
                self.unixtime = restime
                self.msectime = restime * 1000000
                self.mysql    = time
                self.asctime  = parsed[0].strftime(self.tformat).encode('utf-8')
            elif time > 0 and time < 4294967296:                                    # Possible unixtime
                self.original = time
                self.asctime  = datetime.fromtimestamp(time).strftime(self.tformat)
                self.mysql    = datetime.fromtimestamp(time).strftime(self.mysql)
                self.unixtime = time
                self.msectime = time * 1000000
            elif time > 9999999999 and time < 99999999999999999:                    # Possible it is microseconds
                self.original = time
                self.unixtime = int(time/1000000)
                self.asctime  = datetime.fromtimestamp(self.unixtime).strftime(self.tformat) 
                self.msectime = time
                self.mysql    = time
            else: 
                return None
        else:                                                                       # Text format?
            time = time.decode('utf-8')                                             
            parsed = parse(time,  fuzzy_with_tokens=True)
            restime = int(mktime(parsed[0].timetuple()))
            self.original = time.encode('utf-8')
            self.unixtime = restime
            self.msectime = restime * 1000000
            self.mysql    = parsed[0].strftime(self.mysql).encode('utf-8')
            self.asctime  = parsed[0].strftime(self.tformat).encode('utf-8')
        return None

