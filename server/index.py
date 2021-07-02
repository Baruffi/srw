import os
import socket
from concurrent.futures import ThreadPoolExecutor

import toml

from handlers.filehandler import FileHandler
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

sockethandler = SocketHandler(inputs, outputs, message_queues)
filehandler = FileHandler(
    config['folder'], config['prefix'], config['filesize'])


def open_connections():
    global config, server, inputs, sockethandler, filehandler

    while sockethandler.inputs:
        readable, writable, exceptional = sockethandler.select(
            config['timeout'], server)

        for s in readable:
            if s is server:
                sockethandler.accept(s)
            else:
                sockethandler.read(s)

        for s in writable:
            connection, data = sockethandler.write(s)
            if data:
                filehandler.store(connection, data)
                if len(filehandler.content[connection]) >= config['filesize']:
                    filehandler.write(connection)
            else:
                filehandler.write(connection)

        for s in exceptional:
            sockethandler.remove(s)


with ThreadPoolExecutor(max_workers=3) as tpe:
    tpe.submit(open_connections)
    tpe.submit(open_connections)
    tpe.submit(open_connections)
