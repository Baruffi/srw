import os
import socket

import toml

config_path = os.path.join(os.path.dirname(__file__), 'settings/config.toml')
config = toml.load(config_path)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), config['port']))

print(f'Conectado socket do cliente na porta: {config["port"]}')

# s.recv(1024)

fullstring = b''

for i in range(1000):
    new_string = bytes(f'test {i}\n', encoding='utf-8')
    fullstring += new_string
    s.send(new_string)

s.sendall(fullstring)

# s.recv(1024)

s.close()
