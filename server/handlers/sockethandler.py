import select
from socket import socket


class SocketHandler:
    def __init__(self, inputs: set, timeout: float):
        self.inputs = set(inputs)
        self.permanent = set(inputs)
        self.timeout = timeout

    def accept(self, s: socket):
        connection, addr = s.accept()
        socket_ip, _ = addr

        connection.setblocking(False)

        print(f'Conexão aberta com: {socket_ip}')

        self.inputs.add(connection)

        return connection

    def read(self, s: socket):
        data = s.recv(4096)

        if not data:
            self.remove(s, 'Desconexão por parte do cliente.')

        return data

    def select(self):
        readable, _, _ = select.select(
            self.inputs, [], self.inputs, self.timeout)

        timed_out = [
            s for s in self.inputs if s not in self.permanent and s not in readable]

        for s in timed_out:
            self.remove(s, 'Timeout.')

        return readable

    def remove(self, s: socket, reason: str):
        socket_ip, _ = s.getsockname()

        self.inputs.remove(s)

        print(f'Conexão {socket_ip} descartada pelo servidor. Motivo: {reason}')

    def __iter__(self):
        for i in self.inputs:
            yield i
