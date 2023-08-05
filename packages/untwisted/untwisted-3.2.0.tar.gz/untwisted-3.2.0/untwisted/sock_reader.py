from untwisted.event import CLOSE, RECV_ERR, READ, LOAD, SSL_RECV_ERR
from untwisted.errors import CLOSE_ERR_CODE, RECV_ERR_CODE
import socket
import ssl

class SockReader:
    """
    Used to read data through a SuperSocket instance. It spawns LOAD, RECV_ERR or 
    CLOSE.
    """
    
    SIZE = 1024 * 124

    def __init__(self, ssock):
        ssock.add_map(READ, self.update)

    def update(self, ssock):
        """
        """

        try:
            self.process_data(ssock)
        except socket.error as excpt:
            self.process_error(ssock, excpt)

    def process_data(self, ssock):
        data = ssock.recv(self.SIZE)

        if not data: 
            raise socket.error('')
        ssock.drive(LOAD, data)

    def process_error(self, ssock, excpt):
        if not excpt.args[0] in RECV_ERR_CODE:
            ssock.drive(CLOSE, excpt)

class SockReaderSSL(SockReader):
    """    
    Used to read data from a SSL connection. It spawns LOAD, SSL_RECV_ERR
    or CLOSE.
    """

    def update(self, ssock):
        try:
            self.process_data(ssock)
        except ssl.SSLWantReadError as excpt:
            pass
        except ssl.SSLWantWriteError as excpt:
            ssock.drive(SSL_RECV_ERR, ssock, excpt)
        except ssl.SSLError as excpt:
            ssock.drive(CLOSE, ssock, excpt)
        except socket.error as excpt:
            self.process_error(ssock, excpt)

