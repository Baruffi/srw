import os
import socket
import time

import toml

config_path = os.path.join(os.path.dirname(__file__), 'settings/config.toml')
config = toml.load(config_path)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = os.environ['SERVER_HOST'] if 'SERVER_HOST' in os.environ else socket.gethostname()
PORT = int(os.environ['SERVER_PORT']
           ) if 'SERVER_PORT' in os.environ else config['port']

s.connect((HOST, PORT))

print(f'Conectado socket do cliente na porta: {PORT}')

# s.recv(1024)

while ...:
    for i in range(100):
        new_string = bytes(f'test {i}\n', encoding='utf-8')
        s.send(new_string)

    time.sleep(5)

# s.recv(1024)

s.close()
