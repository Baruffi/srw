import os

import toml

config_path = os.path.join(os.path.dirname(__file__), 'config.toml')
config = toml.load(config_path)

PORT = int(os.environ['PORT']) if 'PORT' in os.environ else config['port']
FILESIZE = config['filesize']
PREFIX = config['prefix']
FOLDER = os.environ['FOLDER'] if 'FOLDER' in os.environ else config['folder']
TIMEOUT = config['timeout']
MAX_CONNECTIONS = config['max_connections']
