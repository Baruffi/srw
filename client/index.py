import os
import socket

import toml

config_path = os.path.join(os.path.dirname(__file__), 'settings/config.toml')
config = toml.load(config_path)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), config['port']))

print(f'Conectado socket do cliente na porta: {config["port"]}')

# s.recv(1024)

for i in range(100):
    s.send(bytes(f'test {i} ', encoding='utf-8'))

# s.recv(1024)

s.close()
