import socket
from queue import Queue
from typing import Any

from handlers.filehandler import FileHandler
from handlers.queuehandler import QueueHandler
from handlers.sockethandler import SocketHandler
from settings.config import FILESIZE, FOLDER, PORT, PREFIX, TIMEOUT


def setup_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind((socket.gethostname(), PORT))
    server.listen(5)

    print(f'Aberto socket do servidor na porta: {PORT}')

    return server


def setup_sockethandler(inputs: set[socket.socket]):
    sockethandler = SocketHandler(inputs, TIMEOUT)

    return sockethandler


def setup_functions(message_queues: dict[Any, Queue]):
    filehandler = FileHandler(FOLDER, PREFIX, FILESIZE)
    queuehandler = QueueHandler(message_queues, TIMEOUT)

    def feed(c: socket.socket, data: bytes):
        try:
            queuehandler.feed(c, data)
        except Exception as e:
            print(f'Erro ao alimentar: {e}')

    def consume(c: socket.socket):
        try:
            socket_ip, _ = c.getsockname()

            queuehandler.new(c)

            for message in queuehandler.consume(c):
                try:
                    filehandler.write(socket_ip, message)
                except Exception as e:
                    print(f'Erro ao escrever: {e}')
        except Exception as e:
            print(f'Erro ao consumir: {e}')

    def flush(c: socket.socket):
        try:
            queuehandler.message_queues[c].join()
            queuehandler.remove(c)
        except Exception as e:
            print(f'Erro ao descargar: {e}')

    return feed, consume, flush
