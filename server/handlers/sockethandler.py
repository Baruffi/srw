import queue
import select


class SocketHandler:
    def __init__(self, inputs, outputs, message_queues):
        self.inputs = inputs
        self.outputs = outputs
        self.message_queues = message_queues

    def accept(self, s):
        connection, client_address = s.accept()
        connection.setblocking(False)
        self.inputs.append(connection)
        self.message_queues[connection] = queue.Queue()

    def read(self, s):
        data = s.recv(1024)
        if data:
            self.message_queues[s].put(data)
            if s not in self.outputs:
                self.outputs.append(s)
        else:
            if s in self.outputs:
                self.outputs.remove(s)
            self.inputs.remove(s)
            s.close()
            del self.message_queues[s]

    def write(self, s):
        try:
            next_msg = self.message_queues[s].get_nowait()
        except queue.Empty:
            self.outputs.remove(s)
        else:
            s.send(next_msg)

    def remove(self, s):
        self.inputs.remove(s)
        if s in self.outputs:
            self.outputs.remove(s)
        s.close()
        del self.message_queues[s]

    def select(self):
        readable, writable, exceptional = select.select(
            self.inputs, self.outputs, self.inputs)

        return readable, writable, exceptional
