import os
import socket
from concurrent.futures import ThreadPoolExecutor

import toml

from handlers.filehandler import FileHandler
from handlers.queuehandler import QueueHandler
from handlers.sockethandler import SocketHandler

config_path = os.path.join(os.path.dirname(__file__), 'settings/config.toml')
config = toml.load(config_path)

PORT = config['port']
FILESIZE = config['filesize']
PREFIX = config['prefix']
FOLDER = config['folder']
TIMEOUT = config['timeout']
MAX_CONNECTIONS = config['max_connections']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind((socket.gethostname(), PORT))
server.listen(5)

print(f'Aberto socket do servidor na porta: {PORT}')

inputs = set([server])
outputs = set()
message_queues = {}

with ThreadPoolExecutor(max_workers=MAX_CONNECTIONS) as tpe:
    filehandler = FileHandler(FOLDER, PREFIX, FILESIZE)
    queuehandler = QueueHandler(message_queues, TIMEOUT)
    sockethandler = SocketHandler(
        inputs, TIMEOUT, lambda s: tpe.submit(flush, s))

    def consume(c: socket.socket):
        try:
            socket_ip, _ = c.getsockname()

            for message in queuehandler.consume(c):
                try:
                    filehandler.write(socket_ip, message)
                except Exception as e:
                    print(f'Erro desconhecido ao escrever: {e}')
        except Exception as e:
            print(f'Erro desconhecido ao consumir: {e}')

    def feed(c: socket.socket, data: bytes):
        try:
            queuehandler.feed(c, data)
        except Exception as e:
            print(f'Erro desconhecido ao alimentar: {e}')

    def flush(c: socket.socket):
        try:
            queuehandler.message_queues[c].join()
            queuehandler.remove(c)
        except Exception as e:
            print(f'Erro desconhecido ao descargar: {e}')

    while sockethandler.inputs:
        readable = sockethandler.select()

        for s in readable:
            if s is server and len(sockethandler.inputs) <= MAX_CONNECTIONS:
                c = sockethandler.accept(s)
                queuehandler.new(c)

                tpe.submit(consume, c)
            else:
                if (data := sockethandler.read(s)):
                    tpe.submit(feed, s, data)
