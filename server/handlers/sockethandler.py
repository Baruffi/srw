import select
from socket import socket
from time import time


class SocketHandler:

    def __init__(self, inputs: set[socket], timeout: float):
        self.inputs = set(inputs)
        self.permanent = set(inputs)
        self.timeout = timeout
        self.keep_alive = {}
        self.removed = set()

    def accept(self, s: socket):
        connection, addr = s.accept()
        socket_ip, _ = addr

        connection.setblocking(False)

        print(f'Conexão aberta com: {socket_ip}')

        self.inputs.add(connection)

        return connection, socket_ip

    def read(self, s: socket):
        data = s.recv(4096)

        if not data:
            self.remove(s, 'Desconexão por parte do cliente.')

        return data

    def select(self):
        readable, _, _ = select.select(
            self.inputs, [], self.inputs, self.timeout)

        current_time = time()

        for s in readable:
            if s not in self.permanent:
                self.keep_alive[s] = current_time

        print(f'Keep alive: {len(self.keep_alive)}')

        timed_out = [s for s in self.keep_alive if current_time -
                     self.keep_alive[s] >= self.timeout]

        for s in timed_out:
            self.remove(s, 'Timeout.')

        return readable

    def remove(self, s: socket, reason: str):
        self.inputs.remove(s)
        if s in self.keep_alive:
            del self.keep_alive[s]
        s.close()

        print(f'Conexão fechada pelo servidor. Motivo: {reason}')

        self.removed.add(s)

    def __iter__(self):
        for i in self.inputs:
            yield i
