from concurrent.futures import ThreadPoolExecutor

from settings.config import MAX_CONNECTIONS
from setup import setup_functions, setup_server, setup_sockethandler


def start_server():
    server = setup_server()

    inputs = set([server])
    message_queues = {}

    sockethandler = setup_sockethandler(inputs)
    feed, consume, flush = setup_functions(message_queues)

    with ThreadPoolExecutor(max_workers=MAX_CONNECTIONS) as tpe:
        while sockethandler.inputs:
            readable = sockethandler.select()

            for s in readable:
                if sockethandler.get_addr(s) == sockethandler.SERVER:
                    if len(sockethandler.inputs) <= MAX_CONNECTIONS:
                        c, client_addr = sockethandler.accept(s)

                        tpe.submit(consume, c, client_addr)
                else:
                    if (data := sockethandler.read(s)):
                        tpe.submit(feed, s, data)

            while sockethandler.removed:
                s = sockethandler.removed.pop()
                tpe.submit(flush, s)


if __name__ == '__main__':
    start_server()
