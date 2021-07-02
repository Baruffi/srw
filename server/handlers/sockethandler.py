import queue
import select
from socket import socket

from handlers.filehandler import FileHandler


class SocketHandler:
    def __init__(self, inputs: set, outputs: set, message_queues: dict[socket, queue.Queue], filehandler: FileHandler):
        self.inputs = inputs
        self.outputs = outputs
        self.message_queues = message_queues
        self.filehandler = filehandler

    def accept(self, s: socket):
        connection, addr = s.accept()
        socket_ip, _ = addr

        connection.setblocking(False)

        self.inputs.add(connection)
        self.message_queues[connection] = queue.Queue()
        print(f'Conexão aberta com: {socket_ip}')

    def read(self, s: socket):
        data = s.recv(4096)
        socket_queue = self.message_queues[s]
        socket_ip, _ = s.getsockname()

        self.outputs.add(s)

        if data:
            socket_queue.put(data)
        else:
            self.inputs.remove(s)
            print(f'Conexão {socket_ip} fechada pelo cliente')

    def write(self, s: socket):
        socket_queue = self.message_queues[s]
        socket_ip, _ = s.getsockname()

        self.outputs.remove(s)

        if s not in self.inputs:
            print(f'Conexão morta com: {socket_ip}')
            self.flush(s)
        elif socket_queue.qsize() >= self.filehandler.size:
            self.__write(socket_ip, socket_queue)

    def __write(self, socket_ip, socket_queue: queue.Queue):
        try:
            message = socket_queue.get_nowait()
        except queue.Empty:
            return

        while ...:
            try:
                next_chunk = socket_queue.get_nowait()
                socket_queue.task_done()
                message += next_chunk
            except queue.Empty:
                break

        if message:
            self.filehandler.write(socket_ip, message)

    def flush(self, s: socket):
        socket_queue = self.message_queues[s]
        socket_ip, _ = s.getsockname()

        self.__write(socket_ip, socket_queue)
        self.remove(s)

    def remove(self, s: socket):
        socket_ip, _ = s.getsockname()

        if s in self.inputs:
            self.inputs.remove(s)
        if s in self.outputs:
            self.outputs.remove(s)

        s.close()

        del self.message_queues[s]

        print(f'Conexão {socket_ip} fechada pelo servidor')

    def select(self, timeout: float, *ignore: socket):
        readable, writable, exceptional = select.select(
            self.inputs, self.outputs, self.inputs, timeout)

        timed_out = [
            s for s in self.inputs if s not in readable and s not in writable and s not in exceptional and s not in ignore]
        for s in timed_out:
            socket_ip, _ = s.getsockname()

            print(f'Timeout conexão {socket_ip}')
            self.flush(s)

        return readable, writable, exceptional
