import select
import socket
import time


class Socket:
    def __init__(self):
        self._is_sending_time = None
        self.address = ''
        self.port = 7777
        self.blocking = 0

    def make_tcp_socket(self) -> socket.socket:
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_.setblocking(self.blocking)
        socket_.bind((self.address, self.port))
        socket_.listen(5)
        return socket_

    def send_time(self, socket_: socket.socket) -> None:
        while self._is_sending_time:
            client, address = socket_.accept()
            print('Connected client from {}'.format(address))
            payload = time.ctime(time.time()) + '\n'
            client.send(payload.encode('ascii'))
            client.close()

    def send_time_non_blocking(self, socket_: socket.socket) -> None:
        while self._is_sending_time:
            is_ready = select.select((socket_,), tuple(), tuple(), 1)
            if not is_ready[0]:
                print('Not ready')
                continue
            client, address = socket_.accept()
            print('Connected client from {}'.format(address))
            payload = time.ctime(time.time()) + '\n'
            client.send(payload.encode('ascii'))
            client.close()

    def process(self):
        self._is_sending_time = True
        socket_ = self.make_tcp_socket()

        method = self.send_time if self.blocking == 1 else self.send_time_non_blocking
        try:
            method(socket_)
        except KeyboardInterrupt:
            self._is_sending_time = False
            socket_.close()
            print('Correctly closing')
