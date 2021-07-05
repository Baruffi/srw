from concurrent.futures import ThreadPoolExecutor

from settings.config import MAX_CONNECTIONS
from setup import setup_objects, setup_server


def start_server():
    server = setup_server()
    inputs = set([server])
    message_queues = {}

    with ThreadPoolExecutor(max_workers=MAX_CONNECTIONS) as tpe:
        filehandler, queuehandler, sockethandler, feed, consume, flush = setup_objects(
            inputs, message_queues, tpe)

        while sockethandler.inputs:
            readable = sockethandler.select()

            for s in readable:
                if s is server and len(sockethandler.inputs) <= MAX_CONNECTIONS:
                    c = sockethandler.accept(s)
                    queuehandler.new(c)

                    tpe.submit(consume, c)
                else:
                    if (data := sockethandler.read(s)):
                        tpe.submit(feed, s, data)


if __name__ == '__main__':
    start_server()
