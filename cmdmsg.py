#!/usr/bin/python
# coding=utf-8

# a utility function from dzone.com/snippets
def find_executable(executable, path=None):
    """Try to find 'executable' in the directories listed in 'path' (a
    string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH']).  Returns the complete filename or None if not
    found
    """
    import os, os.path, sys
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    extlist = ['']
    if os.name == 'os2':
        (base, ext) = os.path.splitext(executable)
        # executable files on OS/2 can have an arbitrary extension, but
        # .exe is automatically appended if no dot is present in the name
        if not ext:
            executable = executable + ".exe"
    elif sys.platform == 'win32':
        pathext = os.environ['PATHEXT'].lower().split(os.pathsep)
        (base, ext) = os.path.splitext(executable)
        if ext.lower() not in pathext:
            extlist = pathext
    for ext in extlist:
        execname = executable + ext
        if os.path.isfile(execname):
            return execname
        else:
            for p in paths:
                f = os.path.join(p, execname)
                if os.path.isfile(f):
                    return f
    else:
        return None


# a utility function taken from stackoverflow
def getTerminalSize():
    """
    returns (lines:int, cols:int)
    """
    import os, struct
    def ioctl_GWINSZ(fd):
        import fcntl, termios
        return struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
    # try stdin, stdout, stderr
    for fd in (0, 1, 2):
        try:
            return ioctl_GWINSZ(fd)
        except:
            pass
    # try os.ctermid()
    try:
        fd = os.open(os.ctermid(), os.O_RDONLY)
        try:
            return ioctl_GWINSZ(fd)
        finally:
            os.close(fd)
    except:
        pass
    # try `stty size`
    if find_executable("stty"):
        try:
            size = tuple(int(x) for x in os.popen("stty size", "r").read().split())
            assert len(size) == 2
            return size
        except:
            pass
    # try environment variables
    try:
        return tuple(int(os.getenv(var)) for var in ("LINES", "COLUMNS"))
    except:
        pass
    # i give up. return default.
    return (25, 80)

from datetime import datetime, timedelta
from os.path import commonprefix
from sys import stderr
class cmdmsg():
    def __init__(self, interval = timedelta(0, 1, 0)):
        self.msg = ""
        self.height, self.width = getTerminalSize()
        #print (self.height, self.width)
        self.last = datetime.now()
        self.interval = interval

    def say(self, msg, interval = None):
        if interval == None: interval = self.interval
        if datetime.now() - self.last < interval: return
        self.last = datetime.now()
        # multi-byte characters really futz with this stuff
        msg = msg.replace("\t", " ")
        if len(msg) > (self.width - 1):
            ends = self.width / 2 - 2
            msg = msg[:ends] + "..." + msg[-ends:]
        offset = len(commonprefix([self.msg, msg]))
        # BS moves cursor but doesn't appear to remove content - so print spaces
        if len(self.msg) > len(msg):
            extra = len(self.msg) - len(msg)
            stderr.write("\b" * extra + " " * extra)
            stderr.flush()
        #print (offset, msg, msg[offset:])
        stderr.write("\b" * len(self.msg[offset:]) + msg[offset:])
        stderr.flush()
        self.msg = msg

    def saynow(self, msg):
        self.say(msg, timedelta(0, 0, 0))

    def end(self):
        self.saynow("")

    def spit(self, msg):
        stderr.write("\r" + " " * len(self.msg) + "\r" + msg + "\n" + self.msg)
        stderr.flush()
