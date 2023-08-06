# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class LOG_LEVELS:
    DEBUG = -10
    INFO = 0
    ERROR = 10
    FATAL = 20


class _Logger:
    def printer(self, x):
        print(x)

    def __init__(self, key="--no-key--", log_level=LOG_LEVELS.INFO):
        self.KEY = key
        self.LOG_LEVEL = log_level

    def _do_log(self, message):
        self.printer("[" + str(self.KEY) + "] " + str(message))

    def debug(self, message):
        if self.LOG_LEVEL <= LOG_LEVELS.DEBUG:
            self._do_log(message)

    def info(self, message):
        if self.LOG_LEVEL <= LOG_LEVELS.INFO:
            self._do_log(message)

    def error(self, message):
        if self.LOG_LEVEL <= LOG_LEVELS.ERROR:
            self._do_log(message)

    def fatal(self, message):
        if self.LOG_LEVEL <= LOG_LEVELS.FATAL:
            self._do_log(message)
