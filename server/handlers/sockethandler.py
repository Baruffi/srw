import queue
import select
from socket import socket


class SocketHandler:
    def __init__(self, inputs: set, outputs: set, message_queues: dict[socket, queue.Queue]):
        self.inputs = inputs
        self.outputs = outputs
        self.message_queues = message_queues

    def accept(self, s: socket):
        connection, _ = s.accept()
        connection.setblocking(False)
        self.inputs.add(connection)
        self.message_queues[connection] = queue.Queue()
        print(f'Conexão aberta com: {s.getsockname()[0]}')

    def read(self, s: socket):
        data = s.recv(4096)
        if data:
            self.message_queues[s].put(data)
            self.outputs.add(s)
        else:
            self.inputs.remove(s)
            print(f'Conexão {s.getsockname()[0]} fechada pelo cliente')

    def write(self, s: socket):
        current_queue = self.message_queues[s]
        ip, _ = s.getsockname()
        next_msg = None

        try:
            next_msg = current_queue.get(timeout=5)
        except queue.Empty:
            self.outputs.remove(s)
            print(f'Output da conexão {s.getsockname()[0]} vazio')

            if s not in self.inputs:
                print(f'Conexão morta com: {s.getsockname()[0]}')
                self.remove(s)

        return ip, next_msg

    def remove(self, s: socket):
        sockname = s.getsockname()[0]

        if s in self.inputs:
            self.inputs.remove(s)
        if s in self.outputs:
            self.outputs.remove(s)

        s.close()

        del self.message_queues[s]

        print(f'Conexão {sockname} fechada pelo servidor')

    def select(self, timeout: float, *ignore: socket):
        readable, writable, exceptional = select.select(
            self.inputs, self.outputs, self.inputs, timeout)

        timed_out = [
            s for s in self.inputs if s not in readable and s not in writable and s not in exceptional and s not in ignore]
        for s in timed_out:
            print(f'Timeout cliente {s.getsockname()[0]}')
            self.remove(s)

        return readable, writable, exceptional
