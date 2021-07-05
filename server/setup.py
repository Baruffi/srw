import socket
from concurrent.futures import ThreadPoolExecutor

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


def setup_objects(inputs: set, message_queues: dict, tpe: ThreadPoolExecutor):
    filehandler = FileHandler(FOLDER, PREFIX, FILESIZE)
    queuehandler = QueueHandler(message_queues, TIMEOUT)
    sockethandler = SocketHandler(
        inputs, TIMEOUT, lambda s: tpe.submit(flush, s))

    def feed(c: socket.socket, data: bytes):
        try:
            queuehandler.feed(c, data)
        except Exception as e:
            print(f'Erro desconhecido ao alimentar: {e}')

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

    def flush(c: socket.socket):
        try:
            queuehandler.message_queues[c].join()
            queuehandler.remove(c)
        except Exception as e:
            print(f'Erro desconhecido ao descargar: {e}')

    return filehandler, queuehandler, sockethandler, feed, consume, flush
