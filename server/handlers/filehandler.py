import time


class FileHandler:

    def __init__(self, folder, prefix, size):
        self.folder = folder
        self.prefix = prefix
        self.size = size

    def write(self, data):
        with open(f'{self.folder}/{self.prefix}_{time.time()}', 'wb') as file:
            bytes_written = 0
            while bytes_written < self.size:
                file.write(data[bytes_written:])
                bytes_written += 1

        if len(data) > bytes_written:
            self.write(data[bytes_written:])
