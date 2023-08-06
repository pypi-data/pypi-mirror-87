from untwisted.dispatcher import Erase
from untwisted.sock_writer import SockWriter, SockWriterSSL
from untwisted.sock_reader import SockReader, SockReaderSSL
from untwisted.network import SuperSocket
from untwisted.network import SuperSocketSSL
from untwisted.event import CONNECT, CONNECT_ERR,\
 WRITE, CLOSE, SSL_CONNECT_ERR, SSL_CONNECT

import socket
import ssl

class Client:
    """
    Extension to spawn CONNECT or CONNECT_ERR events.
    """

    def __init__(self, ssock):
        ssock.add_map(WRITE, self.update)

    def update(self, ssock):
        ssock.del_map(WRITE, self.update)
        err = ssock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

        if err != 0:
            ssock.drive(CONNECT_ERR, err)
        else:
            ssock.drive(CONNECT)

class ClientHandshake:
    """ 
    """

    def __init__(self, ssock):
        ssock.add_map(WRITE, self.do_handshake)

    def do_handshake(self, ssock):
        """
        """

        try:
            ssock.do_handshake()
        except ssl.SSLWantReadError:
            pass
        except ssl.SSLWantWriteError:
            pass
        except ssl.SSLError as excpt:
            ssock.drive(SSL_CONNECT_ERR, excpt)
        except socket.error as excpt:
            ssock.drive(SSL_CONNECT_ERR, excpt)
        else:
            ssock.drive(SSL_CONNECT)
            raise Erase

class ClientSSL:
    """
    Extension used to spawn SSL_CONNECT or SSL_CONNECT_ERR events.
    """

    def __init__(self, ssock):
        Client(ssock)
        ssock.add_map(CONNECT, self.update)

    def update(self, ssock):
        ssock.del_map(CONNECT, self.update)
        ClientHandshake(ssock)

def lose(ssock):
    """
    It is used to close TCP connection and unregister
    the SuperSocket instance off the untwisted reactor.

    """

    # First unregister it otherwise it raises an error
    # due to the fd being closed when unregistering off
    # epoll.

    ssock.destroy()
    ssock.close()

def put(ssock, data):
    """
    A handle to be mapped to events like LOAD.
    """

    print(data)

def handle_conerr(ssock, err):
    ssock.destroy()
    ssock.close()

def install_basic_handles(ssock):
    """
    """

    SockWriter(ssock)
    SockReader(ssock)
    ssock.add_map(CLOSE, handle_conerr)

def create_client(addr, port):
    """
    Shorthand function to create a client connection. It installs
    automatically all extensions to send and receive data.

    It also deals with CLOSE event properly.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # First attempt to connect otherwise it leaves
    # an unconnected ssock instance in the reactor.
    sock.connect_ex((addr, port))

    ssock = SuperSocket(sock)
    Client(ssock)
    ssock.add_map(CONNECT, install_basic_handles)
    ssock.add_map(CONNECT_ERR, handle_conerr)
    return ssock

def install_ssl_handles(con):
    SockWriterSSL(con)
    SockReaderSSL(con)
    con.add_map(CLOSE, handle_conerr)

def create_client_ssl(addr, port):
    """
    Shorthand function to set up a SSL connection. It installs all necessary
    extensions to send and receive data over a secured connection.

    This helper function creates a ssl socket with a default context.    
    It also deals with CLOSE event properly.
    """

    sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    wrap    = context.wrap_socket(sock, 
    do_handshake_on_connect=False, server_hostname=addr)

    # First attempt to connect otherwise it leaves
    # an unconnected ssock instance in the reactor.
    wrap.connect_ex((addr, port))
    con = SuperSocketSSL(wrap)

    ClientSSL(con)
    con.add_map(SSL_CONNECT, install_ssl_handles)
    con.add_map(SSL_CONNECT_ERR, handle_conerr)
    con.add_map(CONNECT_ERR, handle_conerr)
    return con
