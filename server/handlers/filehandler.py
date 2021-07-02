import os
import queue
import time


class FileHandler:

    def __init__(self, folder, prefix, size):
        self.folder = folder
        self.prefix = prefix
        self.size = size

    def write(self, current, message):
        path = f'{self.folder}/{current}'

        if not os.path.isdir(path):
            os.mkdir(path)

        self.__write(message, path)

    def __write(self, content, path, sufix=0):
        left, right = content[:self.size], content[self.size:]

        with open(f'{path}/{self.prefix}_{int(time.time())}_{sufix}', 'wb') as file:
            file.write(left)

        if len(right):
            self.__write(right, path, sufix + 1)
