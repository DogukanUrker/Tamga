from datetime import datetime
from time import tzname


def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime():
    return datetime.now().strftime("%H:%M:%S")


def currentTimeZone():
    return tzname[0]


def currentTimeStamp():
    return datetime.now().timestamp()
