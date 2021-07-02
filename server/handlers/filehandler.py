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
        current_time = int(time.time())
        filepath = f'{path}/{self.prefix}_{current_time}_{sufix}'
        size = self.size
        mode = 'wb'

        while os.path.isfile(filepath):
            filesize = os.path.getsize(filepath)
            if filesize >= self.size:
                sufix += 1
                pre, mid, _ = tuple(filepath.split('_'))
                filepath = f'{pre}_{mid}_{sufix}'
            else:
                size = self.size - filesize
                mode = 'ab'
                break

        left, right = content[:size], content[size:]

        with open(filepath, mode) as file:
            file.write(left)

        if len(right):
            self.__write(right, path, sufix + 1)
