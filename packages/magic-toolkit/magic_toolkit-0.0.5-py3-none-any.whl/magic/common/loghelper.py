"""log helper"""

import time

class _LoggerHelper:

    class Severity(object):
        DEBUG, INFO, WARNING, ERROR = range(4)

    level = Severity.INFO  # debug

    @classmethod
    def log(cls, level_, *args):
        stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(stamp, level_, *args)

    @classmethod
    def debug(cls, *args):
        if cls.level <= cls.Severity.DEBUG:
            cls.log("[DEBUG]", *args)

    @classmethod
    def info(cls, *args):
        if cls.level <= cls.Severity.INFO:
            cls.log("[INFO]", *args)

    @classmethod
    def warning(cls, *args):
        if cls.level <= cls.Severity.WARNING:
            cls.log("[WARNING]", *args)

    @classmethod
    def error(cls, *args):
        if cls.level <= cls.Severity.ERROR:
            cls.log("[ERROR]", *args)


def LOG_DEBUG(*args):
    _LoggerHelper.debug(*args)

def LOG_INFO(*args):
    _LoggerHelper.info(*args)

def LOG_WARNING(*args):
    _LoggerHelper.warning(*args)

def LOG_ERROR(*args):
    _LoggerHelper.error(*args)


