import os
import socket
from concurrent.futures import ThreadPoolExecutor

import toml

from handlers.filehandler import FileHandler
from handlers.queuehandler import QueueHandler
from handlers.sockethandler import SocketHandler

config_path = os.path.join(os.path.dirname(__file__), 'settings/config.toml')
config = toml.load(config_path)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind((socket.gethostname(), config['port']))
server.listen(5)

print(f'Aberto socket do servidor na porta: {config["port"]}')

inputs = set([server])
outputs = set()
message_queues = {}

filehandler = FileHandler(
    config['folder'], config['prefix'], config['filesize'])
queuehandler = QueueHandler(message_queues, config['timeout'])
sockethandler = SocketHandler(inputs, config['timeout'])

with ThreadPoolExecutor(max_workers=10) as tpe:
    consumers = {}

    def consume(c: socket.socket):
        socket_ip, _ = c.getsockname()

        for message in queuehandler.consume(c):
            filehandler.write(socket_ip, message)

    def close(c: socket.socket):
        queuehandler.message_queues[c].join()
        queuehandler.remove(c)
        del consumers[c]
        c.close()

    while sockethandler.inputs:
        readable = sockethandler.select()

        for s in readable:
            if s is server:
                c = sockethandler.accept(s)
                queuehandler.new(c)

                consumers[c] = tpe.submit(consume, c)
            else:
                if (data := sockethandler.read(s)):
                    tpe.submit(queuehandler.feed, s, data)

        dead = [c for c in queuehandler if c not in sockethandler]

        for c in dead:
            close(c)  # This can probably also be running on a separate thread, but running it locally and spamming connections can lead to misordered data
