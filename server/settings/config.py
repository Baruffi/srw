import os

import toml

config_path = os.path.join(os.path.dirname(__file__), 'config.toml')
config = toml.load(config_path)

PORT = config['port']
FILESIZE = config['filesize']
PREFIX = config['prefix']
FOLDER = config['folder']
TIMEOUT = config['timeout']
MAX_CONNECTIONS = config['max_connections']
