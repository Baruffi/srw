import select
import time
from socket import socket


class SocketHandler:

    SERVER = 'server'

    def __init__(self, inputs: set[socket], timeout: float):
        self.inputs = dict.fromkeys(
            inputs, (SocketHandler.SERVER, time.time()))
        self.timeout = timeout
        self.removed = set()

    def get_addr(self, s: socket):
        if s in self.inputs:
            return self.inputs[s][0]

    def get_time(self, s: socket):
        if s in self.inputs:
            return self.inputs[s][1]

    def accept(self, s: socket):
        connection, addr = s.accept()
        socket_ip, socket_port = addr
        socket_addr = f'{socket_ip}_{socket_port}'

        connection.setblocking(False)

        print(f'Conexão aberta com: {socket_addr}')

        self.inputs[connection] = socket_addr, time.time()

        return connection, socket_addr

    def read(self, s: socket, amount: int = 4096, chunks: int = 1):
        read_data = b''

        for _ in range(chunks):
            data = s.recv(amount)

            if data:
                read_data += data
            else:
                self.remove(s, 'Desconexão por parte do cliente')
                break

        return read_data

    def remove(self, s: socket, reason: str):
        socket_addr, last_time = self.inputs[s]

        del self.inputs[s]

        s.close()

        print(
            f'Conexão {socket_addr} fechada pelo servidor. Motivo: {reason}. Última atividade: {time.ctime(last_time)}')

        self.removed.add(s)

    def select(self):
        current_time = time.time()

        self.timeout_connections(current_time)

        readable, _, errors = select.select(
            self.inputs, [], self.inputs, self.timeout)

        self.keep_alive(current_time, readable)
        self.handle_errors(errors)

        return readable

    def timeout_connections(self, current_time: float):
        timed_out = []

        for s in self.inputs:
            socket_addr, last_time = self.inputs[s]

            if socket_addr == SocketHandler.SERVER:
                continue

            if current_time - last_time >= self.timeout:
                timed_out.append(s)

        for s in timed_out:
            self.remove(s, 'Timeout')

    def keep_alive(self, current_time: float, alive: list[socket]):
        for s in alive:
            socket_addr, _ = self.inputs[s]
            self.inputs[s] = socket_addr, current_time

        print(f'Keep alive: {len(alive)}')

    def handle_errors(self, errors: list[socket]):
        for s in errors:
            self.remove(s, 'Erro de conexão')

    def __iter__(self):
        for i in self.inputs:
            yield i
