import os
import socket

import toml

config_path = os.path.join(os.path.dirname(__file__), 'settings/config.toml')
config = toml.load(config_path)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), config['port']))
s.send(b'test sent')
print(s.recv(1024))
s.close()
