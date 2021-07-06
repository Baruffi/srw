import os
import time


class FileHandler:

    def __init__(self, base_folder: str, prefix: str, size: int):
        self.base_folder = base_folder
        self.prefix = prefix
        self.size = size

    def write(self, current_folder: str, message: str, start_suffix: int = 0, current_suffix: int = 0):
        current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        file_folder = f'{self.base_folder}/{current_folder}'
        file_name = f'{self.prefix}_{current_time}'
        start_path = f'{file_folder}/{file_name}_{start_suffix}'
        current_path = f'{file_folder}/{file_name}_{current_suffix}'
        max_size = self.size

        if not os.path.isdir(file_folder):
            os.mkdir(file_folder)
        elif os.path.isfile(start_path):
            if os.path.isfile(current_path):
                file_size = os.path.getsize(current_path)
                if file_size >= self.size:
                    current_suffix += 1
                else:
                    max_size = self.size - file_size
        else:
            current_suffix = start_suffix

        return self.__write(max_size, message, file_folder, file_name, current_suffix)

    def __write(self, size: str, message: str, file_folder: str, file_name: str, suffix: int):
        original_size = self.size

        def sub_write(sub_size: str, message: str, suffix: int):
            file_path = f'{file_folder}/{file_name}_{suffix}'
            left, right = message[:sub_size], message[sub_size:]

            with open(file_path, 'ab') as file:
                file.write(left)

            if len(right):
                return sub_write(original_size, right, suffix + 1)
            else:
                return suffix

        return sub_write(size, message, suffix)
