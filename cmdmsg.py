#!/usr/bin/python
# coding=utf-8
from datetime import timedelta
from time import time
from os.path import commonprefix
from sys import stderr
from terminalsize import get_terminal_size


class cmdmsg():
    def __init__(self, interval=timedelta(0, 1, 0)):
        self.msg = ""
        self.width, self.height  = get_terminal_size()
        self.last = None
        self.interval = interval.total_seconds()
        self.silent = self.width is None

    def say(self, msg, interval=None):
        if self.silent:
            return
        if interval is None:
            interval = self.interval
        if self.last is not None and time() - self.last < interval:
            return
        self.last = time()
        # multi-byte characters really futz with this stuff
        msg = msg.replace("\t", " ")
        if len(msg) > (self.width - 1):
            ends = int(self.width / 2 - 2)
            msg = msg[:ends] + "..." + msg[-ends:]
        offset = len(commonprefix([self.msg, msg]))
        # BS moves cursor but doesn't appear to remove content - so print spaces
        if len(self.msg) > len(msg):
            extra = len(self.msg) - len(msg)
            stderr.write("\b" * extra + " " * extra)
            stderr.flush()  # needed on windows
        stderr.write("\b" * len(self.msg[offset:]) + msg[offset:])
        stderr.flush()
        self.msg = msg

    def saynow(self, msg):
        self.say(msg, 0)

    def end(self):
        self.saynow("")

    def spit(self, msg):
        stderr.write("\r" + " " * len(self.msg) + "\r" + msg + "\n" + self.msg)
        stderr.flush()
