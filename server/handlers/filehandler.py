import os
import queue
import time


class FileHandler:

    def __init__(self, folder, prefix, size):
        self.folder = folder
        self.prefix = prefix
        self.size = size
        self.content: dict[str, queue.Queue] = {}

    def store(self, current, data):
        if current not in self.content:
            self.content[current] = queue.Queue()

        self.content[current].put(data)

    def write(self, current):
        if current not in self.content:
            return

        path = f'{self.folder}/{current}'

        if not os.path.isdir(path):
            os.mkdir(path)

        message = self.content[current].get_nowait()

        while ...:
            try:
                next_chunk = self.content[current].get_nowait()
                message += next_chunk
            except queue.Empty:
                break

        print(f'{message=}')

        self.__write(message, path)

        del self.content[current]

    def __write(self, content, path, sufix=0):
        left, right = content[:self.size], content[self.size:]

        with open(f'{path}/{self.prefix}_{int(time.time())}_{sufix}', 'wb') as file:
            file.write(left)

        if len(right):
            self.__write(right, path, sufix + 1)
