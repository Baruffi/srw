import os
import time


class FileHandler:

    def __init__(self, folder, prefix, size):
        self.folder = folder
        self.prefix = prefix
        self.size = size
        self.current = None
        self.content = {}

    def store(self, current, data):
        self.current = current
        self.content[current] = data + self.content.get(current, b'')

    def write(self):
        if self.current not in self.content:
            raise RuntimeError(
                f'Tentativa de escrever em {self.current} sem realizar nenhum store.')

        if not self.content[self.current]:
            return

        path = f'{self.folder}/{self.current}'

        if not os.path.isdir(path):
            os.mkdir(path)

        self.__write(path)

    def __write(self, path: str, sufix=0):
        content = self.content[self.current]
        left, right = content[:self.size], content[self.size:]
        self.content[self.current] = right

        with open(f'{path}/{self.prefix}_{int(time.time())}_{sufix}', 'wb') as file:
            file.write(left)

        if len(right):
            self.__write(path, sufix + 1)
