import time


class TimedSet(set):

    def __init__(self):
        super().__init__()
        self.__table = {}

    def add(self, item, timeout=1):
        self.__table[item] = time.time() + timeout
        set.add(self, item)

    def __contains__(self, item):
        return time.time() < self.__table.get(item)

    def __iter__(self):
        for item in set.__iter__(self):
            if time.time() < self.__table.get(item):
                yield item
