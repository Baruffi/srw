import threading


class ThreadHandler:
    pass


def an_item_is_available():
    pass


def get_an_available_item():
    pass


def make_an_item_available():
    pass


cv = threading.Condition()

with cv:
    cv.wait_for(an_item_is_available)
    get_an_available_item()

with cv:
    make_an_item_available()
    cv.notify()
