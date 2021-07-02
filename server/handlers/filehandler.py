import os
import time


class FileHandler:

    def __init__(self, folder, prefix, size):
        self.folder = folder
        self.prefix = prefix
        self.size = size
        self.content = {}

    def store(self, current, data):
        if current in self.content:
            print(f'{data=}')
            self.content[current] += data
        else:
            self.content[current] = data
            print(f'New data: {data}')
        # self.content[current] = self.content.get(current, b'') + data

    def write(self, current):
        if current not in self.content:
            raise RuntimeError(
                f'Tentativa de escrever em {current} sem realizar nenhum store.')

        if not self.content[current]:
            return

        path = f'{self.folder}/{current}'

        if not os.path.isdir(path):
            os.mkdir(path)

        self.__write(current, path)

    def __write(self, current, path, sufix=0):
        content = self.content[current]
        left, right = content[:self.size], content[self.size:]
        self.content[current] = right

        with open(f'{path}/{self.prefix}_{int(time.time())}_{sufix}', 'wb') as file:
            file.write(left)

        if len(right):
            self.__write(current, path, sufix + 1)
