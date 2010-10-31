#!/usr/bin/python

import email
import os.path
import sys
import re
import datetime
import os

monthmap = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours=1)

class FixedOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(minutes = offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO

def sort_dir(d):
    mdir = os.path.join(d, 'cur')
    odir = os.path.join(d, 'new')

    # Thu, 14 Sep 2006 10:43:29 +0200 (CEST)
    r = re.compile(r"(\w+), +(\d+) (\w+) (\d{4}) "
                   + r"(\d{2}):(\d{2}):(\d{2}) ([+0-9-]+) ?.*")
    rfn = re.compile(r"\d+.\w+.(\w+)[:.](.*)")
    n = 0
    for f in list(os.listdir(mdir)):
        ff = os.path.join(mdir,f)
        e = email.message_from_file(open(ff))

        m = re.match(r, e.get('Date'))
        if not m:
            print e.get('Date')
            return
        tz = FixedOffset(int(m.group(8)), 'Dummy')
        ts = datetime.datetime(int(m.group(4)),
                               int(monthmap[m.group(3)]),
                               int(m.group(2)),
                               int(m.group(5)),
                               int(m.group(6)),
                               int(m.group(7)),
                               tzinfo=tz).strftime("%s")
        try:
            host,flags = re.match(rfn, f).groups()
        except:
            print f
            raise

        n += 1
        fn = "%d.mdsort%d%d.%s:%s" % (int(ts),os.getpid(),n,host,flags)
        
        src = os.path.join(mdir, f)
        dst = os.path.join(odir, fn)
        os.rename(src, dst)

def main():
    sort_dir(sys.argv[1])

if __name__ == '__main__':
    main()
