from queue import Empty, Full, Queue
from typing import Any


class QueueHandler:

    def __init__(self, message_queues: dict[Any, Queue], timeout: float):
        self.message_queues = message_queues
        self.timeout = timeout

    def new(self, queue_key):
        self.message_queues[queue_key] = Queue()

    def put(self, queue_key, data):
        self.message_queues[queue_key].put(data)

    def get(self, queue_key):
        return self.message_queues[queue_key].get()

    def join(self, queue_key):
        self.message_queues[queue_key].join()

    def remove(self, queue_key):
        del self.message_queues[queue_key]

    def feed(self, queue_key, data):
        try:
            self.message_queues[queue_key].put(data, timeout=self.timeout)
        except Full:
            print(f'Queue {queue_key} cheio!')

    def consume(self, queue_key):
        while queue_key in self.message_queues:
            try:
                yield self.message_queues[queue_key].get(timeout=self.timeout)
                self.message_queues[queue_key].task_done()
            except Empty:
                print(
                    f'Queue {queue_key} vazio com {self.message_queues[queue_key].unfinished_tasks} tarefas não finalizadas!')
                break

    def __iter__(self):
        for q in self.message_queues:
            yield q
