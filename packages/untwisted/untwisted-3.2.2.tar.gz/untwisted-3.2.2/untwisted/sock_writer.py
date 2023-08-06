from collections import deque
from untwisted.event import DUMPED, WRITE, CLOSE, READ_ERR
from untwisted.errors import SEND_ERR_CODE
import ssl
import socket

class Dump:
    def process_error(self, ssock, excpt):
        if not excpt.args[0] in SEND_ERR_CODE:
            if not ssock.dead:
                ssock.drive(CLOSE, excpt)

class DumpStr(Dump):
    __slots__ = 'data'

    def __init__(self, data=b''):
        self.data = memoryview(data)

    def process(self, ssock):
        try:
            size = ssock.send(self.data)  
        except socket.error as excpt:
            self.process_error(ssock, excpt)
        else:
            self.data = self.data[size:]

    def __bool__(self):
        return bool(self.data)

class DumpFile(DumpStr):
    __slots__ = 'fd'
    BLOCK     = 1024 * 124

    def __init__(self, fd):
        self.fd = fd
        DumpStr.__init__(self)

    def process(self, ssock):
        if not self.data: 
            self.process_file(ssock)
        DumpStr.process(self, ssock)

    def process_file(self, ssock):
        try:
            data = self.fd.read(DumpFile.BLOCK)
        except IOError as excpt:
            ssock.drive(READ_ERR, excpt)
        else:
            self.data = memoryview(data)

class DumpStrSSL(DumpStr):
    def process(self, ssock):
        # When ssl.SSLEOFError happens it shouldnt spawn CLOSE
        # because there may exist data to be read.
        # If it spawns CLOSE the socket is closed and no data
        # can be read from.
        try:
            size = ssock.send(self.data)  
        except ssl.SSLWantReadError as excpt:
            pass
        except ssl.SSLWantWriteError as excpt:
            pass
        except ssl.SSLEOFError as excpt:
            pass
        except ssl.SSLError as excpt:
            ssock.drive(CLOSE, excpt)
        except socket.error as excpt:
            self.process_error(ssock, excpt)
        else:
            self.data = self.data[size:]

class DumpFileSSL(DumpStrSSL, DumpFile):
    pass

class SockWriter:
    """ 
    Used to write data through a socket asynchronously.
    """

    def __init__(self, ssock):
        """ 
        """

        self.queue = deque()
        self.data  = None
        ssock.dump = self.dump
        self.ssock = ssock
        ssock.dumpfile = self.dumpfile

    def update(self, ssock):
        """
        """
        
        if not self.data: 
            self.process_queue(ssock)

        self.data.process(ssock)

    def process_queue(self, ssock):
        try:
            self.data = self.queue.popleft()
        except IndexError: 
            self.stop()

    def stop(self):
        self.ssock.del_map(WRITE, self.update)
        self.ssock.drive(DUMPED)

    def start(self):
        if not self.queue: 
            self.ssock.add_map(WRITE, self.update)

    def dump(self, data):
        """ 
        Send data through a SuperSocket instance. 
        """

        self.start()
        dump = DumpStr(data)
        self.queue.append(dump)

    def dumpfile(self, fd):
        """ 
        Dump a file through a SuperSocket instance. 
        """

        self.start()
        dump = DumpFile(fd)
        self.queue.append(dump)

class SockWriterSSL(SockWriter):
    """
    Used to dump data through a SuperSocket instance.
    """

    def dump(self, data):
        self.start()
        data = DumpStrSSL(data)
        self.queue.append(data)

    def dumpfile(self, fd):
        self.start()
        fd = DumpFileSSL(fd)
        self.queue.append(fd)

